"""module that interact with database. Currently interface with MongoDB is
being implemented. Will support SQLite and Amazon DynamoDB in the future."""

from pymongo import MongoClient
from parajumper.config import Config
from parajumper.item import Item
CONF = Config()
if CONF.options['database']['kind'] == 'mongodb':
    CLIENT = MongoClient(CONF.options['database']['location'])
    DATABASE = CLIENT[CONF.options['database']['db_name']]
    ITEM_T = DATABASE.items

def save_item_mongodb(item, table=ITEM_T, database=DATABASE):
    """Save item to database. Return id of the corresponding record.

    item: an Item instance.
    table: table/collection to store items.
    database: name of database."""
    try:
        identity = table.find_one({"_id": item.identity})['_id']
        table.update({"_id": identity}, item.__dict__)
    except AttributeError:
        identity = table.insert_one(item.__dict__).inserted_id
    return identity

def load_item_mongodb(record_id, table=ITEM_T, database=DATABASE):
    """Load item from database. Return an Item object.

    record_id: id for finding the item.
    table: table/collection from which record is read.
    database: name of database."""
    result = Item()
    record = table.find_one({"_id": record_id})
    for key in record.keys():
        setattr(result, key, record[key])
    return result

def save_item(item, table=ITEM_T, database=DATABASE):
    """Wrapper function for saving item."""
    if CONF.options['database']['kind'] == 'mongodb':
        save_item_mongodb(item, table, database)

def load_item(record_id, table=ITEM_T, database=DATABASE):
    """Wrapper function for saving item."""
    if CONF.options['database']['kind'] == 'mongodb':
        load_item_mongodb(record_id, table, database)
