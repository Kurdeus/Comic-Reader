from os import makedirs, path
from configparser import ConfigParser
import appdirs
from app.utils.Constants import Constant

class ConfigManager:
    @staticmethod
    def load_config() -> ConfigParser:
    
        config = ConfigParser()
        setattr(config, 'optionxform', lambda x: x)  # preserve case of keys

        # create the config path if it doesn't exist
        user_path = appdirs.user_data_dir(Constant.TEMP_DIR, appauthor=False)
        makedirs(user_path, exist_ok=True)
        config_path = path.join(user_path, 'config.ini')

        config.read(config_path)

        dirty = False
        if not Constant.CONFIG_SECTION in config:
            config[Constant.CONFIG_SECTION] = {}
            dirty = True
        if not 'browser' in config[Constant.CONFIG_SECTION]:
            config[Constant.CONFIG_SECTION]['browser'] = ''
            dirty = True
        if not 'disableNavButtons' in config[Constant.CONFIG_SECTION]:
            config[Constant.CONFIG_SECTION]['disableNavButtons'] = 'no'
            dirty = True
        if not 'disableNavBar' in config[Constant.CONFIG_SECTION]:
            config[Constant.CONFIG_SECTION]['disableNavBar'] = 'no'
            dirty = True
        if not 'dynamicImageLoading' in config[Constant.CONFIG_SECTION]:
            config[Constant.CONFIG_SECTION]['dynamicImageLoading'] = 'no'
            dirty = True
        if dirty:
            with open(config_path, 'w') as config_file:
                config.write(config_file)
        return config

    @staticmethod
    def has_background_tasks(config: ConfigParser) -> bool:
        return not config[Constant.CONFIG_SECTION].getboolean('disableNavBar')
