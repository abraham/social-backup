"""Fetch answers from StackExchange."""


import copy
from datetime import datetime
import requests


class Answers:

    """Fetch answers from StackExchange."""

    _namespace = 'stackexchange:answers'
    _id_key = 'answer_id'
    _totalItems = 0
    _key = None
    _access_token = None
    _page = 1
    _has_more = True
    _maxErrors = 5
    _totalErrors = 0

    def __init__(self, key, accessToken, site):
        """Fetch answers from StackExchange."""
        self._key = key
        self._access_token = accessToken
        self._site = site

    def _getItems(self):
        url = 'https://api.stackexchange.com/2.2/me/answers'
        params = {
            'key': self._key,
            'access_token': self._access_token,
            'site': self._site,
            'filter': '!LfC50Kmo3--9GqYMmOl1JH',
            'sort': 'activity',
            'order': 'desc',
            'pagesize': 100,
            'page': self._page,
        }

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

        self._page += 1
        self._has_more = response.json()['has_more']
        return response.json()['items']

    def mutateItem(self, item):
        """Mutate an item for uniformity."""
        mutated = copy.deepcopy(item)
        created = datetime.fromtimestamp(item['creation_date'])
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
        if self._has_more is False:
            return []
        items = self._getItems()
        self._totalItems += len(items)
        return items

    def reset(self):
        """Reset counters to start anew."""
        self._totalItems = 0
        self._page = 1
        self._has_more = True
        self._maxErrors = 5
        self._totalErrors = 0
