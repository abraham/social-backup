"""Fetch activities from Google+."""


import httplib2
from oauth2client import client
from apiclient import discovery, errors
from apiclient.discovery import build
from datetime import datetime
import copy


class Plus:

    """Interact with the Google+ API."""

    _totalItems = 0
    _developerKey = None
    _userId = None
    _maxResults = 100
    _maxErrors = 5
    _totalErrors = 0
    _nextPageToken = None
    _http = httplib2.Http()
    _service = None
    _namespace = 'plus'
    _id_key = 'id'

    def __init__(self, developerKey, userId):
        """Interact with the Google+ API."""
        self._developerKey = developerKey
        self._userId = userId
        self._service = build('plus', 'v1', http=self._http,
                              developerKey=self._developerKey)

    def _getItems(self):

        params = {
            'userId': self._userId,
            'collection': 'public',
            'maxResults': self._maxResults,
            'pageToken': self._nextPageToken,
        }

        try:
            response = self._service.activities().list(**params).execute()
        except errors.HttpError as e:
            if totalErrors < maxErrors:
                remainingErrors = maxErrors - totalErrors
                print e
                print 'Encountered error, will retry', remainingErrors, 'times'
                totalErrors += 1
                return self._getItems()
            else:
                print 'Encountered to many errors'
                raise e

        self._nextPageToken = response.get('nextPageToken', False)
        return response.get('items', [])

    def getIdKey(self):
        """Get the network native key for id."""
        return self._id_key

    def getNamespace(self):
        """Get the network namespace."""
        return self._namespace

    def mutateItem(self, item):
        """Mutate an item for uniformity."""
        mutated = copy.deepcopy(item)
        format = '%Y-%m-%dT%H:%M:%S.%f'
        created = datetime.strptime(mutated['published'][:-1], format)
        mutated['_'] = {
            'created': created,
            'ns': self._namespace,
        }
        return mutated

    def getTotalItems(self):
        """Get the total number of Google+ activities fetched."""
        return self._totalItems

    def getItems(self):
        """Get recent Google+ activities."""
        items = self._getItems()
        self._totalItems += len(items)
        if len(items) == 0 and self._nextPageToken is False:
            return None
        else:
            return items

    def reset(self):
        """Reset counters to start anew."""
        self._totalItems = 0
        self._nextPageToken = None
        self._maxErrors = 5
        self._totalErrors = 0
