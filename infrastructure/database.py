from pymongo import MongoClient
from pymongo.database import Database


def get_database(config: dict) -> Database:
    db = config['db']
    host = config.get('host', 'localhost')
    port = config.get('port', '27017')
    uri = f'{host}:{port}'
    if not config.get('mock', False):
        username = config['username']
        password = config['password']
        uri = f'{username}:{password}@{uri}/?authSource=admin'

    client = MongoClient(f'mongodb://{uri}', tz_aware=True)
    return client[db]
