import base64
from configparser import ConfigParser
import json
import os
from string import Template
import tempfile
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union
from pathlib import Path
from shutil import copy
from app.service.ImageAdapter import ImageProcessor
from app.utils.Constants import Constant
from app.utils.excepts import NoImagesFoundError



class HtmlGenerator:
    @staticmethod
    def create_html(
        paths: Iterable[Union[Path, str]],
        thumbnails: Iterable[Optional[Path]],
        version: str,
        title: str,
        doc_template: str,
        page_template: str,
        config: ConfigParser,
        outfile: str = os.path.join(tempfile.gettempdir(), Constant.TEMP_DIR, 'render.html'),
    ) -> str:
        """Render a list of image paths to the finished HTML document.

        Parameters:
        * `paths`: full file:// paths to images to render on the page.
        * `version`: version number to render on page.
        * `title`: title of the page.
        * `doc_template`: HTML template for the overall document.
        * `page_template`: HTML template for each comic page element.
        * `config`: parsed `config.ini` file.
        * `outfile`: path to write the rendered document to. Defaults to OS temp directory.

        Returns: path to rendered HTML document.

        Throws: `NoImagesFoundError` if the image list is empty.
        """
        if not paths:
            raise NoImagesFoundError('No images were sent to the renderer.')
        try:
            write_config = json.dumps(
                {
                    'disableNavButtons': config[Constant.CONFIG_SECTION].getboolean('disableNavButtons'),
                    'disableNavBar': config[Constant.CONFIG_SECTION].getboolean('disableNavBar'),
                    'dynamicImageLoading': config[Constant.CONFIG_SECTION].getboolean('dynamicImageLoading'),
                }
            )
        except:
            write_config = '{}'
        with open(outfile, 'w', encoding='utf-8', newline='\r\n') as renderfd:
            html_template = Template(doc_template)
            img_template = Template(page_template)
            img_dimensions = [ImageProcessor.get_dimensions(path) for path in paths]
            img_list = [
                img_template.substitute(
                    img=(
                        Path(path).as_uri()
                        if not config[Constant.CONFIG_SECTION].getboolean('dynamicImageLoading')
                        else Constant.EMPTY_IMAGE
                    ),
                    lazyimg=(
                        Path(path).as_uri()
                        if config[Constant.CONFIG_SECTION].getboolean('dynamicImageLoading')
                        else ''
                    ),
                    thumbnail=thumbnail.as_uri() if thumbnail else Constant.EMPTY_IMAGE,
                    width=dimensions[0] if dimensions else 0,
                    height=dimensions[1] if dimensions else 0,
                    id=str(i),
                    previd=str(i - 1) if i > 0 else 'none',
                    nextid=str(i + 1) if i < len(list(paths)) - 1 else 'none',
                )
                for i, (path, thumbnail, dimensions) in enumerate(
                    zip(paths, thumbnails, img_dimensions)
                )
            ]
            doc_string = html_template.substitute(
                pages=''.join(img_list),
                version=version,
                title=title,
                config=base64.b64encode(write_config.encode('utf-8')).decode('utf-8'),
            )
            renderfd.write(doc_string)
        return outfile

    @staticmethod
    def create_bootstrap(outfile: str, render: str, index: int, boot_template: str) -> str:
        """Render the bootstrap document, which redirects to the main HTML document at the opened image.
        This is required because an HTML bookmark link cannot be used as a file:// URI.

        Parameters:
        * `outfile`: path to write the rendered document to.
        * `render`: path to the main HTML document.
        * `index`: the image number to jump to in the main document after redirect.
        * `boot_template`: HTML template for the bootstrap document.

        Returns: path to the rendered bootstrap document.
        """
        with open(outfile, 'w', encoding='utf-8', newline='\r\n') as bootfd:
            html_boot = Template(boot_template).substitute(document=render, index=str(index))
            bootfd.write(html_boot)
        return outfile

    @staticmethod
    def copy_assets(src_paths: Iterable[Union[Path, str]], dest_path: Path) -> None:
        """Copy all files pointed by src_paths to destination."""
        for src in src_paths:
            copy(src, dest_path)

