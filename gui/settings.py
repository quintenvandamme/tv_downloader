import configparser
import os
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return relative_path

class Settings:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self._create()
        self._read()

    def _create(self):
        # Create the settings file if it doesn't exist
        if not os.path.exists(resource_path('data/settings/settings.ini')):
            self.config['Settings'] = {
                'download_path': os.path.expanduser('~')
            }

            # create the directory data/settings if it doesn't exist
            if not os.path.exists(resource_path('data/settings')):
                os.makedirs(resource_path('data/settings'))

            with open(resource_path('data/settings/settings.ini'), 'w') as configfile:
                self.config.write(configfile)
            return True

    def _read(self):
        self.config.read(resource_path('data/settings/settings.ini'))

    def get(self, section, key):
        self._read()
        return self.config[section][key]
    
    def set(self, section, key, value):
        self.config[section][key] = value
        with open(resource_path('data/settings/settings.ini'), 'w') as configfile:
            self.config.write(configfile)