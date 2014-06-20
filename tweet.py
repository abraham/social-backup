"""Fetch tweets from Twitter."""


import copy
from datetime import datetime
import twitter


class Tweet:

    """Interact with the Twitter API."""

    _namespace = 'twitter'
    _id_key = 'id_str'
    _totalItems = 0
    _consumer_key = None
    _consumer_secret = None
    _access_token_key = None
    _access_token_secret = None
    _user_id = None
    _count = 200
    _since_id = None
    _max_id = None
    _maxErrors = 5
    _totalErrors = 0
    _api = None

    def __init__(self, consumerKey, consumerSecret, accessTokenKey,
                 accessTokenSecret, userId):
        """Interact with the Twitter API."""
        self._consumer_key = consumerKey
        self._consumer_secret = consumerSecret
        self._access_token_key = accessTokenKey
        self._access_token_secret = accessTokenSecret
        self._user_id = userId
        self._api = twitter.Api(consumer_key=self._consumer_key,
                                consumer_secret=self._consumer_secret,
                                access_token_key=self._access_token_key,
                                access_token_secret=self._access_token_secret)

    def _getItems(self):
        items = []
        try:
            response = self._api.GetUserTimeline(user_id=self._user_id,
                                                 max_id=self._max_id,
                                                 count=self._count,
                                                 include_rts=True,
                                                 exclude_replies=False)
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

        items = [item.AsDict() for item in response]
        self._max_id = items[-1]['id_str']
        for item in items:
            if item.get('urls', None) is not None:
                del item['urls']
            if item.get('retweeted_status', {}).get('urls', None) is not None:
                del item['retweeted_status']['urls']
        return items

    def mutateItem(self, item):
        """Mutate an item for uniformity."""
        mutated = copy.deepcopy(item)
        format = '%a %b %d %H:%M:%S +0000 %Y'
        created = datetime.strptime(item['created_at'], format)
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
        """Get the total number of Twitter statuses fetched."""
        return self._totalItems

    def getItems(self):
        """Get recent Twitter statuses."""
        items = self._getItems()
        self._totalItems += len(items)
        if len(items) == 0 and self._nextPageToken is False:
            return None
        else:
            return items

    def reset(self):
        """Reset counters to start anew."""
        self._totalItems = 0
        self._since_id = None
        self._max_id = None
        self._maxErrors = 5
        self._totalErrors = 0
