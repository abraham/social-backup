"""Backup personal social activities."""


import os
import time
from config import Config
from plus import Plus
from tweet import Tweet as Twitter
from github import GitHub
from terminal import Terminal
from disk import Disk
from mongo import Mongo


services = {}
storages = {}
config = Config(file_name=os.environ['CONFIG_FILE_NAME'])


if 'plus' in config.get('enabledServices'):
    services['plus'] = Plus(**config.get('plus'))
if 'twitter' in config.get('enabledServices'):
    services['twitter'] = Twitter(**config.get('twitter'))
if 'github' in config.get('enabledServices'):
    services['github'] = GitHub(**config.get('github'))


if 'terminal' in config.get('enabledStorages'):
    storages['terminal'] = Terminal(**config.get('terminal'))
if 'disk' in config.get('enabledStorages'):
    storages['disk'] = Disk(**config.get('disk'))
if 'mongo' in config.get('enabledStorages'):
    storages['mongo'] = Mongo(**config.get('mongo'))


while True:
    """Craw for stuffs."""
    totalItems = 0

    print 'starting saving', config.get('paginationLimit'), 'items from', \
        services.keys(), 'to', storages.keys()

    for service in services:
        items = []

        while (config.get('paginationLimit') > services[service].getTotalItems()):
            items = services[service].getItems()
            totalItems += len(items)

            for item in items:
                mutated = services[service].mutateItem(item)

                for storage in storages:
                    use_mutated = config.get(storage)['mutationEnabled']
                    storages[storage].saveItem(namespace=service,
                                               id_key=services[service].getIdKey(),
                                               item=mutated if use_mutated else item)

            print 'fetched and saved', services[service].getTotalItems(), service, \
                'items of', config.get('paginationLimit')

    print 'Finished saving items', totalItems, 'to', storages.keys()

    print '===================='
    print 'sleeping for', config.get('sleep'), 'minutes'

    time.sleep(int(config.get('sleep')) * 60)
