from os import makedirs, path
import sys
import tempfile
from shutil import rmtree
from typing import Any, Dict
from app.utils.Constants import Constant


class SystemUtils:
    """Service for file operations."""
    
    @staticmethod
    def setup_temp_directory() -> str:
        """Set up temporary directory for comic rendering."""
        temp_dir = path.join(tempfile.gettempdir(), Constant.TEMP_DIR)
        rmtree(temp_dir, ignore_errors=True)
        makedirs(temp_dir, exist_ok=True)
        return temp_dir

    

    
    @staticmethod
    def get_templates_info(working_dir: str) -> Dict[str, Any]:
        """Get template paths and assets information."""
        lib_dir = f'{working_dir}'
        return {
            'doc_template_path': f'{lib_dir}/{Constant.DOC_TEMPLATE}',
            'page_template_path': f'{lib_dir}/{Constant.PAGE_TEMPLATE}',
            'boot_template_path': f'{lib_dir}/{Constant.BOOT_TEMPLATE}',
            'asset_paths': (f'{lib_dir}/{asset}' for asset in Constant.STATIC_FILES),
            'img_types': Constant.SUPPORTED_IMAGES
        }
