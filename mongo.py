"""Save stuffs to MongoDB."""


from pymongo import MongoClient


import os
import io
import json


class Mongo:

    """Save stuffs to MongoDB."""

    def __init__(self, connection, dBName, mutationEnabled):
        """Save stuffs to MongoDB."""
        self.__connection = "%s/%s" % (connection, dBName)
        self.__dBName = dBName
        self.__db = MongoClient(self.__connection)[self.__dBName]

    def saveItem(self, namespace, id_key, item):
        """Save item to MongoDB."""
        _id = '%s:%s' % (namespace, item[id_key])

        query = {
            '_id': _id,
        }

        doc = item
        doc['_id'] = _id

        params = {
            'upsert': True,
        }

        self.__db.posts.update(query, doc, **params)
