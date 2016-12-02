"""module that interact with database. Currently interface with MongoDB is
being implemented. Will support SQLite and Amazon DynamoDB in the future."""

from pymongo import MongoClient
from parajumper.config import Config
from parajumper.item import Item, ITEMS_DICT
CONF = Config()
if CONF.options['database']['kind'] == 'mongodb':
    CLIENT = MongoClient(CONF.options['database']['location'])
    DATABASE = CLIENT[CONF.options['database']['db_name']]
    ITEM_T = DATABASE.items
    BINDER_T = DATABASE.binders

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
    ITEMS_DICT[result.identity] = result
    return result

def remove_item_mongodb(record_id, table=ITEM_T):
    """Remove record from database.

    record_id: id of the record to remove.
    table: collection the record resides in.
    database: database object."""
    table.remove({"identity": record_id})
    ITEMS_DICT.pop(record_id, None)

def save_binder_mongodb(binder, table=BINDER_T, item_table=ITEM_T):
    """Save a binder to database. Return its uuid.
    If any member of the binder is not saved, save them first.

    binder: binder to save.
    item_table: collection to save items."""
    for identity in binder.members:
        save_item(ITEMS_DICT[identity], item_table)
    if table.find_one({"identity": binder.identity}) is not None:
        table.update({"identity": binder.identity}, binder.__dict__)
    else:
        table.insert_one(binder.__dict__)
    return binder.identity

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

def save_binder(binder, table=BINDER_T):
    """Wrapper function for saving binder."""
    if CONF.options['database']['kind'] == 'mongodb':
        return save_binder_mongodb(binder, table)
