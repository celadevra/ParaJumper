"""module that interact with database. Currently interface with MongoDB is
being implemented. Will support SQLite and Amazon DynamoDB in the future."""

from pymongo import ASCENDING
from parajumper.config import DBConfig
from parajumper.item import Item, ITEMS_DICT
from parajumper.binder import Binder, BINDERS_DICT
from parajumper.indices import gen_index

def save_item_mongodb(item, conf=DBConfig()):
    """Save item to database. Return id of the corresponding record.

    item: an Item instance.
    table: table/collection to store items.
    database: database object."""
    for key in item.__dict__:
        conf.item_t.update_one({"identity": item.identity},
                               {"$set": {key: item.__dict__[key]}},
                               upsert=True)
    gen_index(item.identity, item.content)
    return item.identity

def load_item_mongodb(record_id, conf=DBConfig()):
    """Load item from database. Return an Item object.

    record_id: id for finding the item.
    table: table/collection from which record is read.
    database: database object."""
    result = Item()
    ITEMS_DICT.pop(result.identity)
    record = conf.item_t.find_one({"identity": record_id})
    for key in record:
        if key != '_id':
            setattr(result, key, record[key])
    ITEMS_DICT[record['identity']] = result
    return result

def remove_item_mongodb(record_id, conf=DBConfig()):
    """Remove record from database.

    record_id: id of the record to remove.
    table: collection the record resides in.
    database: database object."""
    conf.item_t.remove({"identity": record_id})
    ITEMS_DICT.pop(record_id, None)

def save_binder_mongodb(binder, conf=DBConfig()):
    """Save a binder to database. Return its uuid.
    If any member of the binder is not saved, save them first.

    binder: binder to save.
    item_table: collection to save items."""
    if binder.members is not None:
        for identity in binder.members:
            save_item(ITEMS_DICT[identity])
    if conf.binder_t.find_one({"identity": binder.identity}) is not None:
        for key in binder.__dict__:
            conf.binder_t.update_one({"identity": binder.identity}, {"$set": {key: binder.__dict__[key]}})
    else:
        conf.binder_t.insert_one(binder.__dict__)
    return binder.identity

def remove_binder_mongodb(binder_identity, conf=DBConfig()):
    """Remove a binder from database.

    binder_identity: binder to remove."""
    conf.binder_t.remove({"identity": binder_identity})
    BINDERS_DICT.pop(binder_identity, None)

def load_binder_mongodb(record_id, conf=DBConfig()):
    """Load a binder from database.

    record_id: identity of binder to load."""
    result = Binder()
    BINDERS_DICT.pop(result.identity)
    record = conf.binder_t.find_one({"identity": record_id})
    for key in record.keys():
        setattr(result, key, record[key])
    BINDERS_DICT[record['identity']] = result
    return result

def search_by_date_mongodb(date_from, date_to, conf=DBConfig()):
    """Search items that are scheduled in a time range
    from date_from to date_to. Return a list of item identities."""
    if date_from > date_to:
        date_to, date_from = date_from, date_to
    result = []
    items = conf.item_t.find({"schedule":{'$gte': date_from, '$lte': date_to}},
                       sort=[('schedule', ASCENDING)])
    for thing in items:
        result.append(thing['identity'])
    return result

def search_by_tag_mongodb(tags, conf=DBConfig()):
    """Search items with a certain tag. Return a list of item identities.

    tags: an array of input tags"""
    result = []
    items = conf.item_t.find({"tags":{'$in': tags}}, sort=[('schedule', ASCENDING)])
    for thing in items:
        result.append(thing['identity'])
    return result

def search_mongodb(terms, conf=DBConfig()):
    """Search items with certain term. Return a list of item identities."""
    result = []
    items = conf.index_t.find({"words":{"$in": terms}})
    for thing in items:
        result.append(thing['identity'])
    return result

def save_item(item, conf=DBConfig()):
    """Wrapper function for saving item."""
    if conf.kind == 'mongodb':
        return save_item_mongodb(item)

def load_item(record_id, conf=DBConfig()):
    """Wrapper function for loading item."""
    if conf.kind == 'mongodb':
        return load_item_mongodb(record_id)

def remove_item(record_id, conf=DBConfig()):
    """Wrapper function for removing item."""
    if conf.kind == 'mongodb':
        return remove_item_mongodb(record_id)

def save_binder(binder, conf=DBConfig()):
    """Wrapper function for saving binder."""
    if conf.kind == 'mongodb':
        return save_binder_mongodb(binder)

def remove_binder(binder, conf=DBConfig()):
    """Wrapper function for removing binder."""
    if conf.kind == 'mongodb':
        return remove_binder_mongodb(binder)

def load_binder(record_id, conf=DBConfig()):
    """Wrapper function for loading binder from db."""
    if conf.kind == 'mongodb':
        return load_binder_mongodb(record_id)

def search_by_date(date_from, date_to, conf=DBConfig()):
    """Wrapper function for loading items of a certain date from db."""
    if conf.kind == 'mongodb':
        return search_by_date_mongodb(date_from, date_to)

def search_by_tag(tags, conf=DBConfig()):
    """Wrapper function for loading items of a certain tag from db."""
    if conf.kind == 'mongodb':
        return search_by_tag_mongodb(tags)

def search(terms, conf=DBConfig()):
    """Wrapper function for searching terms in item content."""
    if conf.kind == 'mongodb':
        return search_mongodb(terms)
