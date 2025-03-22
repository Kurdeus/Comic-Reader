from typing import Union, Optional, Tuple, Iterable
from pathlib import Path
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from app.service.ProgressAdapter import ProgressIndicator
# Image Processing
class ImageProcessor:
    @staticmethod
    def get_dimensions(path: Union[Path, str]) -> Optional[Tuple[int, int]]:
        """Get the pixel dimensions (width, height) of an image file.

        Returns None if file is not a valid image.
        """
        try:
            with Image.open(path) as img:
                return img.size
        except:
            return None

    @staticmethod
    def generate_thumbnails(
        paths: Iterable[Union[Path, str]],
        outpath: Path,
        progress_bar: Optional[ProgressIndicator] = None,
    ) -> Iterable[Path]:
        """Create thumbnails for all images in paths and save them to outpath."""
        executor = ThreadPoolExecutor(max_workers=cpu_count() - 1)

        # Render thumbnails in parallel. No need to await these since the webapp can be started before
        # this is completed. The last task to be completed exits the program
        def task(path: Union[Path, str]):
            path = Path(path)
            try:
                with Image.open(path) as img:
                    img.thumbnail((2000, 360), Image.Resampling.NEAREST)
                    img.save(outpath / f'{path.stem}_thumbnail.png')
            except:
                pass
            finally:
                if progress_bar:
                    progress_bar.increment()

        for p in paths:
            executor.submit(task, p)
        return ((outpath / f'{Path(path).stem}_thumbnail.png') for path in paths)
