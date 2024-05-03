import configparser
import os
import sys

settings_file_dir = os.path.join(os.path.expanduser('~'), '.config', 'tvdownloader')
settings_file_path = os.path.join(settings_file_dir, 'settings.ini')

class Settings:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self._create()
        self._read()

    def _create(self):
        # Create the settings file if it doesn't exist

        if not os.path.exists(settings_file_path):
            self.config['Settings'] = {
                'download_path': os.path.expanduser('~')
            }

            # create the directory data/settings if it doesn't exist
            if not os.path.exists(settings_file_dir):
                os.makedirs(settings_file_dir)

            with open(settings_file_path, 'w') as configfile:
                self.config.write(configfile)
            return True

    def _read(self):
        self.config.read(settings_file_path)

    def get(self, section, key):
        self._read()

        if not self.config.has_section(section):
            self.set(section, key, '')
            return ''
        else:
            if self.config[section].get(key) is None:
                self.set(section, key, '')
                return ''
            else:
                return self.config[section][key]
    
    def set(self, section, key, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        
        if not self.config.has_option(section, key):
            self.config.set(section, key, value)

        self.config[section][key] = value
        with open(settings_file_path, 'w') as configfile:
            self.config.write(configfile)