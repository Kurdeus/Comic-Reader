from pathlib import Path
from configparser import ConfigParser
import webbrowser
from app.utils.Constants import Constant


class Browser:
    """Service for opening the rendered comic in a web browser."""
    
    @staticmethod
    def open_in_browser(boot_path: Path, config: ConfigParser) -> None:
        """Open the rendered comic in a web browser."""
        if config[Constant.CONFIG_SECTION]['browser']:
            webbrowser.register(
                config[Constant.CONFIG_SECTION]['browser'],
                None,
                instance=webbrowser.GenericBrowser(config[Constant.CONFIG_SECTION]['browser']),
                preferred=True,
            )
        webbrowser.get().open(boot_path.as_uri())
