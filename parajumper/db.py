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

def save_item_mongodb(item, table=ITEM_T):
    """Save item to database. Return id of the corresponding record.

    item: an Item instance.
    table: table/collection to store items.
    database: database object."""
    if table.find_one({"identity": item.identity}) is not None:
        table.update({"identity": item.identity}, item.__dict__)
    else:
        table.insert_one(item.__dict__)
    return item.identity

def load_item_mongodb(record_id, table=ITEM_T):
    """Load item from database. Return an Item object.

    record_id: id for finding the item.
    table: table/collection from which record is read.
    database: database object."""
    result = Item()
    record = table.find_one({"identity": record_id})
    for key in record.keys():
        setattr(result, key, record[key])
    return result

def remove_item_mongodb(record_id, table=ITEM_T):
    """Remove record from database.

    record_id: id of the record to remove.
    table: collection the record resides in.
    database: database object."""
    table.remove({"identity": record_id})

def save_item(item, table=ITEM_T):
    """Wrapper function for saving item."""
    if CONF.options['database']['kind'] == 'mongodb':
        return save_item_mongodb(item, table)

def load_item(record_id, table=ITEM_T):
    """Wrapper function for loading item."""
    if CONF.options['database']['kind'] == 'mongodb':
        return load_item_mongodb(record_id, table)

def remove_item(record_id, table=ITEM_T):
    """Wrapper function for removing item."""
    if CONF.options['database']['kind'] == 'mongodb':
        return remove_item_mongodb(record_id, table)
