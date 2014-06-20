"""Fetch events from GitHub."""


import copy
from datetime import datetime
import requests


class GitHub:

    """Fetch events from GitHub."""

    _namespace = 'github'
    _id_key = 'id'
    _totalItems = 0
    _client_id = None
    _client_secret = None
    _user = None
    _next_link = None
    _maxErrors = 5
    _totalErrors = 0

    def __init__(self, clientId, clientSecret, userId):
        """Fetch events from GitHub."""
        self._client_id = clientId
        self._client_secret = clientSecret
        self._user_id = userId

    def _parseLinkHeader(self, header):
        links = {}
        for part in header.split(','):
            ref = part.split(';')[1].split('=')[1].strip()[1:-1]
            link = part.split(';')[0].strip()[1:-1]
            links[ref] = link
        return links

    def _getItems(self):
        if self._next_link is None:
            url = 'https://api.github.com/user/%s/events/public' % (self._user_id, )
            params = {
                'client_id': self._client_id,
                'client_secret': self._client_secret,
            }
        else:
            url = self._next_link
            params = {}

        try:
            response = requests.get(url, params=params)
        except Exception as e:
            if self._totalErrors < self._maxErrors:
                remainingErrors = self._maxErrors - self._totalErrors
                print e
                print 'Encountered error, will retry', remainingErrors, 'times'
                self._totalErrors += 1
                return self._getItems()
            else:
                print 'Encountered to many errors'
                raise e

        link = self._parseLinkHeader(response.headers['link'])
        if link.get('next', None) is not None:
            self._next_link = link['next']
        else:
            self._next_link = False

        return response.json()

    def mutateItem(self, item):
        """Mutate an item for uniformity."""
        mutated = copy.deepcopy(item)
        format = '%Y-%m-%dT%H:%M:%S'
        created = datetime.strptime(item['created_at'][:-1], format)
        mutated['_'] = {
            'created': created,
            'ns': self._namespace,
        }
        return mutated

    def getIdKey(self):
        """Get the network native key for id."""
        return self._id_key

    def getNamespace(self):
        """Get the network namespace."""
        return self._namespace

    def getTotalItems(self):
        """Get the total number of GitHub events fetched."""
        return self._totalItems

    def getItems(self):
        """Get recent GitHub events."""
        if self._next_link is False:
            return []
        items = self._getItems()
        self._totalItems += len(items)
        return items

    def reset(self):
        """Reset counters to start anew."""
        self._totalItems = 0
        self._next_link = None
        self._maxErrors = 5
        self._totalErrors = 0
