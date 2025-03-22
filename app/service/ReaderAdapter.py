import tempfile
from configparser import ConfigParser
from pathlib import Path
from typing import Iterable, Optional
import py7zr
import rarfile
import zipfile
from app.service.HtmlAdapter import HtmlGenerator
from app.utils.Constants import Constant
from app.service.ImageAdapter import ImageProcessor
from app.service.ProgressAdapter import ProgressIndicator
from app.service.ArchiveAdapter import ArchiveExtractor
from app.utils.excepts import NoImagesFoundError
from app.service.FileAdapter import FileHandler
from app.utils.Constants import Constant



class ComicProcessor:
    @staticmethod
    def process_and_render(
        path: str,
        version: str,
        doc_template_path: str,
        page_template_path: str,
        boot_template_path: str,
        asset_paths: Iterable[str],
        img_types: Iterable[str],
        config: ConfigParser,
        progress_bar: ProgressIndicator,
        outpath: Path = Path(tempfile.gettempdir()) / Constant.TEMP_DIR,
    ) -> Path:
        """Main controller procedure. Handles opening of archive, image, or directory and renders the images
        appropriately for each, then opens the document in the user's default browser.

        Parameters:
        * `path`: path to image, directory, or archive.
        * `version`: version of the app to display to user.
        * `doc_template_path`: path to HTML template for the main document.
        * `page_template_path`: path to HTML template for individual comic page elements.
        * `boot_template_path`: path to HTML template for bootstrap document.
        * `asset_paths`: paths of static assets to copy.
        * `img_types`: list of recognized image file extensions.
        * `config`: parsed `config.ini` file.
        * `progress_bar`: progress bar UI to update.
        * `outpath`: directory to write temporary files in. Defaults to OS temp directory.

        Returns: Path to the bootstrap document, which can be opened in a web browser.

        Throws:
        * `BadZipFile`: opened file was a zip file, but could not be read.
        * `BadRarFile`: opened file was a rar file, but could not be read.
        * `Bad7zFile`: opened file was a 7z file, but could not be read.
        * `NoImagesFoundError`: if no images could be found in an opened directory or archive.
        """
        start = 0
        pPath = Path(path).resolve()
        doc_template, page_template, boot_template = (
            FileHandler.load_template(p) for p in (doc_template_path, page_template_path, boot_template_path)
        )
        try:
            if pPath.is_file():
                if pPath.suffix.lower()[1:] in img_types:
                    imgpaths = FileHandler.find_images(pPath.parent, img_types)
                    start = imgpaths.index(pPath)
                    title = pPath.parent.name
                else:
                    try:
                        imgpaths = ArchiveExtractor.extract_archive(pPath, img_types, str(outpath))
                        title = pPath.name
                    except zipfile.BadZipFile as e:
                        raise zipfile.BadZipfile(
                            f'"{path}" does not appear to be a valid zip/cbz file.'
                        ).with_traceback(e.__traceback__)
                    except rarfile.BadRarFile as e:
                        raise rarfile.BadRarFile(
                            f'"{path}" does not appear to be a valid rar/cbr file.'
                        ).with_traceback(e.__traceback__)
                    except py7zr.Bad7zFile as e:
                        raise py7zr.Bad7zFile(
                            f'"{path}" does not appear to be a valid 7z/cb7 file.'
                        ).with_traceback(e.__traceback__)
            else:
                imgpaths = FileHandler.find_images(path, img_types)
                title = pPath.name
            FileHandler.ensure_output_dir(outpath)
            HtmlGenerator.copy_assets(asset_paths, outpath)
            if not config[Constant.CONFIG_SECTION].getboolean('disableNavBar'):
                progress_bar.set_total(len(imgpaths))
                thumbnail_paths: Iterable[Optional[Path]] = ImageProcessor.generate_thumbnails(
                    imgpaths, outpath, progress_bar
                )
            else:
                thumbnail_paths = (None for _ in imgpaths)
                progress_bar.tk_root.after_idle(lambda: progress_bar.tk_root.destroy())

            renderfile = HtmlGenerator.create_html(
                paths=imgpaths,
                thumbnails=thumbnail_paths,
                version=version,
                title=title,
                doc_template=doc_template,
                page_template=page_template,
                outfile=str(outpath / 'index.html'),
                config=config,
            )
            bootfile = HtmlGenerator.create_bootstrap(
                outfile=str(outpath / 'boot.html'),
                render=Path(renderfile).as_uri(),
                index=start,
                boot_template=boot_template,
            )
            return Path(bootfile)

        except NoImagesFoundError:
            raise