import os
import tempfile
from typing import Union
from typing import Iterable, List, Union
import zipfile
import py7zr
import rarfile
from pathlib import Path
from app.utils.Constants import Constant
from app.utils.excepts import NoImagesFoundError
from app.service.FileAdapter import FileHandler

class SevenZipWrapper:
    """
    Minimal wrapper class over py7zr.SevenZipFile to support zipfile-like interface.
    """

    def __init__(self, file: Union[Path, str], mode: str = 'r'):
        self._file = py7zr.SevenZipFile(str(file), mode)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._file.close()

    def namelist(self):
        return self._file.getnames()

    def extractall(self, path=None, members=None):
        self._file.extractall(path)


class ArchiveExtractor:
    @staticmethod
    def extract_files(
        img_types: Iterable[str],
        archive: Union[zipfile.ZipFile, rarfile.RarFile, SevenZipWrapper],
        outpath: str = os.path.join(tempfile.gettempdir(), Constant.TEMP_DIR),
    ) -> List[Path]:
        """Extract image files in archive to the outpath."""
        imagefiles = list(filter(lambda f: f.split('.')[-1].lower() in img_types, archive.namelist()))
        if not imagefiles:
            raise NoImagesFoundError()
        archive.extractall(outpath, imagefiles)
        return [Path(outpath) / image for image in sorted(imagefiles, key=FileHandler.natural_sort_key)]

    @staticmethod
    def extract_archive(
        path: Path,
        img_types: Iterable[str],
        outpath: str = os.path.join(tempfile.gettempdir(), Constant.TEMP_DIR),
    ) -> List[Path]:
        """Extract image files found in an archive file.

        Parameters:
        * `path`: path to archive.
        * `img_types`: list of recognized image file extensions.
        * `outpath`: directory to extract images to. Defaults to OS temp directory.

        Returns: list of absolute paths to extracted image files.

        Throws:
        * `NoImagesFoundError` if no images were found in the archive.
        * `BadZipFile` if CBZ/ZIP archive could not be read.
        * `BadRarFile` if CBR/RAR archive could not be read.
        * `Bad7zFile` if CB7/7Z archive could not be read.
        """
        file_ext = path.suffix.lower()[1:]
        try:
            if file_ext in Constant.ZIP_FORMATS:
                with zipfile.ZipFile(path, mode='r') as zip_file:
                    return ArchiveExtractor.extract_files(img_types, zip_file, outpath)
            elif file_ext in Constant.RAR_FORMATS:
                with rarfile.RarFile(path, mode='r') as rar_file:
                    return ArchiveExtractor.extract_files(img_types, rar_file, outpath)
            elif file_ext in Constant.SEVEN_ZIP_FORMATS:
                with SevenZipWrapper(path, mode='r') as _7z_file:
                    return ArchiveExtractor.extract_files(img_types, _7z_file, outpath)
            else:
                raise NoImagesFoundError(f'Unknown archive format: {path}')
        except NoImagesFoundError:
            raise NoImagesFoundError(f'No image files were found in archive: {path}')
