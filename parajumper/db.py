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
    database: database object."""
    try:
        identity = table.find_one({"_id": item._id})['_id']
        table.update({"_id": identity}, item.__dict__)
    except TypeError:
        identity = table.insert_one(item.__dict__).inserted_id
    return identity

def load_item_mongodb(record_id, table=ITEM_T, database=DATABASE):
    """Load item from database. Return an Item object.

    record_id: id for finding the item.
    table: table/collection from which record is read.
    database: database object."""
    result = Item()
    record = table.find_one({"_id": record_id})
    for key in record.keys():
        setattr(result, key, record[key])
    return result

def remove_item_mongodb(record_id, table=ITEM_T, database=DATABASE):
    """Remove record from database.
    
    record_id: id of the record to remove.
    table: collection the record resides in.
    database: database object."""
    table.remove({"_id": record_id})

def save_item(item, table=ITEM_T, database=DATABASE):
    """Wrapper function for saving item."""
    if CONF.options['database']['kind'] == 'mongodb':
        return save_item_mongodb(item, table, database)

def load_item(record_id, table=ITEM_T, database=DATABASE):
    """Wrapper function for loading item."""
    if CONF.options['database']['kind'] == 'mongodb':
        return load_item_mongodb(record_id, table, database)

def remove_item(record_id, table=ITEM_T, database=DATABASE):
    """Wrapper function for removing item."""
    if CONF.options['database']['kind'] == 'mongodb':
        return remove_item_mongodb(record_id, table, database)
