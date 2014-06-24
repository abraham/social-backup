"""Fetch media like on Instagram."""

def _import_non_local(name, custom_name=None):
    import imp
    import sys

    custom_name = custom_name or name

    f, pathname, desc = imp.find_module(name, sys.path[1:])
    module = imp.load_module(custom_name, f, pathname, desc)
    # f.close()

    return module


instagram_api = _import_non_local('instagram', 'instagram_api')
from instagram_api.bind import InstagramAPIError
from instagram_api.client import InstagramAPI as api
import copy
from datetime import datetime


class Liked:

    """Fetch media like on Instagram."""

    _api_user = None
    _api = None
    _totalItems = 0
    _client_id = None
    _client_secret = None
    _user_id = None
    _access_token = None
    _count = 33
    _max_count = 120
    _maxErrors = 5
    _totalErrors = 0
    _next = None
    _namespace = 'instagram:liked'
    _id_key = 'id'
    _user_visibility = {}

    def __init__(self, clientId, clientSecret, userId, accessToken):
        """Fetch media like on Instagram."""
        self._client_id = clientId
        self._client_secret = clientSecret
        self._user_id = userId
        self._access_token = accessToken
        self._api_user = api(access_token=self._access_token)
        self._api = api(client_id=self._client_id, client_secret=self._client_secret)

    def _is_user_private(self, user_id):
        if self._user_visibility.get(user_id, None) is None:
            try:
                self._api.user(user_id)
                self._user_visibility[user_id] = False
            except InstagramAPIError as error:
                self._user_visibility[user_id] = True
        return self._user_visibility[user_id]

    def _getItems(self):
        try:
            response, self._next = self._api_user.user_liked_media(return_json=True,
                                                                   count=self._count,
                                                                   with_next_url=self._next)
        except:
            if totalErrors < maxErrors:
                remainingErrors = maxErrors - totalErrors
                print e
                print 'Encountered error, will retry', remainingErrors, 'times'
                totalErrors += 1
                return self._getItems()
            else:
                print 'Encountered to many errors'
                raise e

        for item in response:
            item['private'] = self._is_user_private(item['user']['id'])
        return response

    def getIdKey(self):
        """Get the network native key for id."""
        return self._id_key

    def getNamespace(self):
        """Get the network namespace."""
        return self._namespace

    def mutateItem(self, item):
        """Mutate an item for uniformity."""
        mutated = copy.deepcopy(item)
        created = datetime.fromtimestamp(int(item['created_time']))
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
        self._max_count = 0
        self._next = None
