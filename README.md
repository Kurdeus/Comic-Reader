# Comic Reader

Comic Reader is a lightweight, streamlined image viewer specifically designed for reading digital comics, manga, and other image-based content. It transforms images from a folder or archive (ZIP/CBZ/RAR/CBR/7Z/CB7 formats) into a single, continuously scrollable page that opens in your default web browser.



## Features

- View your images in a continuously scrollable page.
- Various automatic resizing options.
- Horizontal view options (LTR and RTL)
- Use all the familiar navigation controls available on your browser/device setup.
- Open images directly from a folder or contained in a comic book archive file.
  - Supported archive formats: cbz, cbr, cb7, zip, rar, 7z
  - Supported image formats: bmp, png, jpg, gif, apng, svg, webp
- Light and dark themes.
- Invert color of images.

## Installation

Download the latest version from the [Releases](https://github.com/Kurdeus/Comic-Reader/releases) page.

Simply extract the downloaded file to any location on your computer. No installation process is required - the application is ready to use immediately.

## Usage

You can start Comic Reader in several ways:

- Run `ComicReader.exe` (Windows) and open an image file or comic book archive
- Right-click an image file or archive and select "Open with..." to choose the Comic Reader executable
- Drag and drop an image file, folder of images, or archive onto the Comic Reader executable or shortcut

## Advanced Configuration

Beyond the in-app settings, additional options can be configured in the `config.ini` file (the file is automatically generated the first time you run the application):

- Windows: `C:\Users\<username>\AppData\Local\temp-comicreader\config.ini`

### Available config.ini Options

- **browser** (default: none): *Windows only* - specify a browser for the app to use. Leave empty to use your system's default browser.
  - Example (Windows): `browser = C:\Program Files\Google\Chrome\Application\chrome.exe`
  
- **disableNavButtons** (default: no): hide the next/previous page navigation controls.
  - Example: `disableNavButtons = yes`
- **disableNavBar** (default: no): disable the right-side quick navigation bar. This can improve loading speed for large image collections.
  - Example: `disableNavBar = yes`
- **dynamicImageLoading** (default: no): reduce memory usage by unloading images that aren't currently visible. Helpful for large collections but may affect scrolling performance.
  - Example: `dynamicImageLoading = yes`

## For Developers

### Prerequisites

- Python 3.7 or newer
- PyInstaller: `pip install pyinstaller` (only needed for building the executable)

### Setup

After ensuring the prerequisites are installed:

1. Clone the repository
2. Install Python dependencies: `pip install -r requirements.txt`

### Building a Distributable

The executable is built using [PyInstaller](https://www.pyinstaller.org/).

#### Windows

Run the `build-win.cmd` script. The executable will be created in the `dist` directory.

PyInstaller options can be customized in the script. See the [PyInstaller documentation](https://pyinstaller.readthedocs.io/en/stable/usage.html) for more details.


### ❤️ Thanks To :
- [**luejerry**](https://github.com/luejerry) : for writing the original code for this project.
- [**Kurdeus**](https://github.com/Kurdeus) : for maintaining the project and adding new features.