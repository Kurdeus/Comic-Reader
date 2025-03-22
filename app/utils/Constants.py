

# Constants
class Constant:
    APP_NAME = 'Comic Reader'
    SUPPORTED_IMAGES = {'jpg', 'png', 'apng', 'bmp', 'jpeg', 'gif', 'svg', 'webp'}
    ZIP_FORMATS = {'zip', 'cbz'}
    RAR_FORMATS = {'rar', 'cbr'}
    SEVEN_ZIP_FORMATS = {'7z', 'cb7'}
    STATIC_FILES = {
        'assets/styles.css',
        'assets/scripts.js',
        'assets/zenscroll.js',
        'assets/menu.svg',
        'assets/menu-light.svg',
        'assets/scroll.svg',
        'assets/scroll-light.svg',
        'assets/roboto-bold.woff2',
        'assets/roboto-regular.woff2',
    }
    DOC_TEMPLATE = 'assets/doc.template.html'
    PAGE_TEMPLATE = 'assets/img.template.html'
    BOOT_TEMPLATE = 'assets/boot.template.html'
    EMPTY_IMAGE = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8HwYAAloBV80ot9EAAAAASUVORK5CYII='
    CONFIG_SECTION = 'comicreader'
    VERSION = '0.0.1'
    TEMP_DIR = 'temp-comicreader'

