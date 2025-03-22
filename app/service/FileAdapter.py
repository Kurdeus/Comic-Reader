from typing import Any, List, Union, Iterable
import re
from pathlib import Path
from app.utils.excepts import NoImagesFoundError

class FileHandler:
    @staticmethod
    def natural_sort_key(filename: Union[str, Path]) -> List[Any]:
        """Natural sort comparison key function for filename sorting."""
        return [int(s) if s.isdigit() else s.lower() for s in re.split(r'(\d+)', str(filename))]

    @staticmethod
    def find_images(path: Union[str, Path], img_types: Iterable[str]) -> List[Path]:
        """Get a list of image file paths from a directory.

        Parameters:
        * `path`: directory to scan for images.
        * `img_types`: list of recognized image file extensions.

        Returns: list of absolute paths to image files.

        Throws: `NoImagesFoundError` if no images were found in the directory.
        """
        files = filter(lambda f: f.is_file(), Path(path).iterdir())
        imagefiles = list(filter(lambda f: f.suffix.lower()[1:] in img_types, files))
        if not imagefiles:
            raise NoImagesFoundError(f'No image files were found in directory "{Path(path).resolve()}"')
        return [
            p if p.is_absolute() else p.resolve() for p in sorted(imagefiles, key=FileHandler.natural_sort_key)
        ]

    @staticmethod
    def ensure_output_dir(outpath: Path) -> None:
        """Create the output directory for the rendered page files. If outpath is a file, it is deleted."""
        if outpath.exists() and outpath.is_file():
            outpath.unlink()
        outpath.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def load_template(path: Union[Path, str]) -> str:
        """Load the file at path a a UTF-8 string."""
        with open(path, encoding='utf-8') as template_file:
            return template_file.read()

