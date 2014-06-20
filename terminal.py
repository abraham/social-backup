"""Print stuffs."""


class Terminal:

    """Print stuffs."""

    def __init__(self, **args):
        """Print stuffs."""
        pass

    def saveItem(self, namespace, id_key, item):
        """Print item to terminal."""
        print 'New', namespace, 'item with id', item[id_key]
        print item
        print '=========='
