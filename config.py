"""Read, parse, and handle JSON config files."""

import os
import sys
import json


class Config:

    """Read, parse, and handle JSON config files."""

    _config = None

    def __init__(self, file_name):
        """Read and parse a JSON config file."""
        cofig_path = os.path.join(os.path.dirname(__file__), file_name)

        try:
            config_file = open(cofig_path, 'r')
        except:
            sys.exit('Unable to read config file.')

        config_str = config_file.read()

        try:
            config = json.loads(config_str)
        except:
            sys.exit('Unable to parse JSON.')

        self._config = config

        self._parseEnv()

    def get(self, name):
        """Get a config value."""
        return self._config.get(name, None)

    def _parseEnv(self):
        """Iterate environ and overwrite config.json values."""
        for key in os.environ:
            parts = key.split('_')
            if parts[0] == 'BACKUP' and len(parts) == 3:
                self._config[parts[1]][parts[2]] = os.environ[key]
            elif parts[0] == 'BACKUP' and len(parts) == 2:
                self._config[parts[1]] = os.environ[key]
