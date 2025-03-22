from argparse import ArgumentParser, Namespace
import platform
from tkinter import Tk

class ArgumentParserHandler:

    @staticmethod
    def parse_args() -> Namespace:
        """Parse command line arguments."""
        parser = ArgumentParser(description='Comic Reader')
        parser.add_argument('path', nargs='?', help='Path to image, folder, or comic book archive')
        parser.add_argument('--no-browser', action='store_true')
        return parser.parse_args()

    @staticmethod
    def get_platform_args() -> Namespace:
        """
        Get program arguments based on platform. On Windows, arguments are obtained directly via
        command line args. On MacOS, arguments must be obtained from an Open Document (`odoc`) event
        sent by the OS Launch Services.
        """
        cli_args = ArgumentParserHandler.parse_args()
        if platform.system() == 'Darwin' and not cli_args.path:
            # MacOS only: when launching by drag-dropping a file to the app icon or using Open With
            # menu, the app does not receive the file path in the command line arguments. To work
            # around this, we create a temporary Tk window to catch the OpenDocument event that
            # provides the file path to open
            tk = Tk()

            def set_path(*args):
                cli_args.path = args[0]
                tk.destroy()

            tk.createcommand('::tk::mac::OpenDocument', set_path)
            # If no event is received in 10ms, assume app was launched without a file to open
            tk.after(10, lambda: tk.destroy())
            tk.mainloop()
        return cli_args
