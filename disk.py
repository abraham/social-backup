"""Save stuffs to disk."""


import os
import io
import json


class Disk:

    """Save stuffs to disk."""

    def __init__(self, mutationEnabled, directory='data'):
        """Save stuffs to disk."""
        self._directory = directory

    def _getPath(self, namespace, name):
        parts = (os.path.dirname(__file__), self._directory, namespace,
                 '%s.json' % (name, ))
        return os.path.join(*parts)

    def saveItem(self, namespace, id_key, item):
        """Save JSON blob to disk."""
        path = self._getPath(namespace, item[id_key])
        with io.open(path, 'w', encoding='utf-8') as f:
            f.write(unicode(json.dumps(item, ensure_ascii=False)))
