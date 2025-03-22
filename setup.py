import sys
import traceback
from tkinter import Tk, filedialog, messagebox
from typing import Any, Dict
from os import path
from app.service.ArgumentAdapter import ArgumentParserHandler
from app.service.ConfigAdapter import ConfigManager
from app.service.ReaderAdapter import ComicProcessor
from app.utils.Constants import Constant
from app.service.ProgressAdapter import ProgressIndicator
from app.service.SystemUtilsAdapter import SystemUtils
from app.service.BrowserAdapter import Browser


class ComicReaderApp:
    """Presenter for the user interface."""
    
    def __init__(self):
        self.tk = Tk()
        self.tk.resizable(width=False, height=False)
        self.tk.title(Constant.APP_NAME)
        self.tk.geometry('400x50')  # Slightly taller to accommodate the enhanced progress bar

        
        self.version = Constant.VERSION
        self.config_manager = ConfigManager()
        self.system_utils = SystemUtils()
        self.config = self.config_manager.load_config()
        self.comic_processor = ComicProcessor()
        self.browser = Browser()
        self.system_adapter = SystemUtils()
        self.args = ArgumentParserHandler.get_platform_args()
        self.progress_bar = ProgressIndicator(self.tk)
  
    
    def show_error(self, exception: Exception) -> None:
        """Show error message to the user."""
        messagebox.showerror(
            'Comic Reader encountered an error: ' + type(exception).__name__,
            ''.join(traceback.format_exc()),
        )
    

    
    def open_file_picker(self) -> str:
        """Open file picker dialog."""
        imagetypes = [f'.{ext}' for ext in Constant.SUPPORTED_IMAGES]
        archivetypes = [
            f'.{ext}' for ext in (*Constant.ZIP_FORMATS, *Constant.RAR_FORMATS, *Constant.SEVEN_ZIP_FORMATS)
        ]
        filetypes = (
            ('Supported files', [*imagetypes, *archivetypes]),
            ('Images', imagetypes),
            ('Comic book archive', archivetypes),
            ('All files', ['*']),
        )
        return filedialog.askopenfilename(
            filetypes=filetypes,
            title='Open Image - Comic Reader',
        )
    

    def open_manga(self, target_path: str, no_browser: bool, templates_info: Dict[str, Any], version: str) -> None:
        """Open and render manga from the given path."""
        try:
            boot_path = self.comic_processor.process_and_render(
                target_path, 
                version, 
                templates_info['doc_template_path'], 
                templates_info['page_template_path'], 
                templates_info['boot_template_path'], 
                templates_info['asset_paths'], 
                templates_info['img_types'], 
                self.config, 
                self.progress_bar
            )
            
            if no_browser:
                print(boot_path)
            else:
                self.browser.open_in_browser(boot_path, self.config)
                
        except Exception as e:
            self.show_error(e)
        finally:
            if not self.config_manager.has_background_tasks(self.config):
                self.tk.destroy()



    def setup_app(self):
        if not self.args.path:
            target_path = self.open_file_picker()
            if not target_path:
                return
        else:
            target_path = self.args.path
        
            # Set up working environment
        working_dir = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
        
        templates_info = self.system_adapter.get_templates_info(working_dir)
        self.system_adapter.setup_temp_directory()

        def run_app():
            self.open_manga(target_path, self.args.no_browser, templates_info, self.version)
        
        self.tk.after(0, run_app)
        self.tk.mainloop()
    









if __name__ == '__main__':
    app = ComicReaderApp()
    app.setup_app()