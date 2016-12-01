"""module that interact with database. Currently interface with MongoDB is
being implemented. Will support SQLite and Amazon DynamoDB in the future."""

from pymongo import MongoClient
from parajumper.config import Config
CONF = Config()
if CONF.options['database']['kind'] == 'mongodb':
    CLIENT = MongoClient(CONF.options['database']['location'])
