"""module that interact with database. Currently interface with MongoDB is
being implemented. Will support SQLite and Amazon DynamoDB in the future."""

from datetime import date, datetime, timedelta
from pymongo import ASCENDING
from parajumper.config import DBConfig
from parajumper.item import Item, ITEMS_DICT
from parajumper.binder import Binder, BINDERS_DICT
from parajumper.indices import gen_index

def save_item_mongodb(item):
    """Save item to database. Return id of the corresponding record.

    item: an Item instance.
    table: table/collection to store items.
    database: database object."""
    conf = DBConfig()
    for key in item.__dict__:
        conf.item_t.update_one({"identity": item.identity},
                               {"$set": {key: item.__dict__[key]}},
                               upsert=True)
    gen_index(item.identity, item.content)
    return item.identity

def load_item_mongodb(record_id):
    """Load item from database. Return an Item object.

    record_id: id for finding the item.
    table: table/collection from which record is read.
    database: database object."""
    conf = DBConfig()
    result = Item()
    ITEMS_DICT.pop(result.identity)
    record = conf.item_t.find_one({"identity": record_id})
    for key in record:
        if key != '_id':
            setattr(result, key, record[key])
    ITEMS_DICT[record['identity']] = result
    return result

def remove_item_mongodb(record_id):
    """Remove record from database.

    record_id: id of the record to remove.
    table: collection the record resides in.
    database: database object."""
    conf = DBConfig()
    conf.item_t.remove({"identity": record_id})
    ITEMS_DICT.pop(record_id, None)

def save_binder_mongodb(binder):
    """Save a binder to database. Return its uuid.
    If any member of the binder is not saved, save them first.

    binder: binder to save.
    item_table: collection to save items."""
    conf = DBConfig()
    if binder.members is not None:
        for identity in binder.members:
            save_item(ITEMS_DICT[identity])
    if conf.binder_t.find_one({"identity": binder.identity}) is not None:
        for key in binder.__dict__:
            conf.binder_t.update_one({"identity": binder.identity},
                                     {"$set": {key: binder.__dict__[key]}})
    else:
        conf.binder_t.insert_one(binder.__dict__)
    return binder.identity

def remove_binder_mongodb(binder_identity):
    """Remove a binder from database.

    binder_identity: binder to remove."""
    conf = DBConfig()
    conf.binder_t.remove({"identity": binder_identity})
    BINDERS_DICT.pop(binder_identity, None)

def load_binder_mongodb(record_id):
    """Load a binder from database.

    record_id: identity of binder to load."""
    conf = DBConfig()
    result = Binder()
    BINDERS_DICT.pop(result.identity)
    record = conf.binder_t.find_one({"identity": record_id})
    for key in record.keys():
        setattr(result, key, record[key])
    BINDERS_DICT[record['identity']] = result
    return result

def search_by_date_mongodb(date_from, date_to):
    """Search items that are scheduled in a time range
    from date_from to date_to. Return a list of item identities."""
    conf = DBConfig()
    if date_from > date_to:
        date_to, date_from = date_from, date_to
    result = []
    items = conf.item_t.find({"schedule":{'$gte': date_from, '$lte': date_to}},
                             sort=[('schedule', ASCENDING)])
    for thing in items:
        result.append(thing['identity'])
    return result

def search_by_tag_mongodb(tags):
    """Search items with a certain tag. Return a list of item identities.

    tags: an array of input tags"""
    conf = DBConfig()
    result = []
    items = conf.item_t.find({"tags":{'$in': tags}}, sort=[('schedule', ASCENDING)])
    for thing in items:
        result.append(thing['identity'])
    return result

def search_mongodb(terms):
    """Search items with certain term. Return a list of item identities."""
    conf = DBConfig()
    result = []
    items = conf.index_t.find({"words":{"$in": terms}})
    for thing in items:
        result.append(thing['identity'])
    return result

def save_item(item):
    """Wrapper function for saving item."""
    conf = DBConfig()
    if conf.kind == 'mongodb':
        return save_item_mongodb(item)

def load_item(record_id):
    """Wrapper function for loading item."""
    conf = DBConfig()
    if conf.kind == 'mongodb':
        return load_item_mongodb(record_id)

def remove_item(record_id):
    """Wrapper function for removing item."""
    conf = DBConfig()
    if conf.kind == 'mongodb':
        return remove_item_mongodb(record_id)

def save_binder(binder):
    """Wrapper function for saving binder."""
    conf = DBConfig()
    if conf.kind == 'mongodb':
        return save_binder_mongodb(binder)

def remove_binder(binder):
    """Wrapper function for removing binder."""
    conf = DBConfig()
    if conf.kind == 'mongodb':
        return remove_binder_mongodb(binder)

def load_binder(record_id):
    """Wrapper function for loading binder from db."""
    conf = DBConfig()
    if conf.kind == 'mongodb':
        return load_binder_mongodb(record_id)

def search_by_date(date_from, date_to):
    """Wrapper function for loading items of a certain date from db."""
    conf = DBConfig()
    if conf.kind == 'mongodb':
        return search_by_date_mongodb(date_from, date_to)

def search_by_tag(tags):
    """Wrapper function for loading items of a certain tag from db."""
    conf = DBConfig()
    if conf.kind == 'mongodb':
        return search_by_tag_mongodb(tags)

def search(terms):
    """Wrapper function for searching terms in item content."""
    conf = DBConfig()
    if conf.kind == 'mongodb':
        return search_mongodb(terms)

def create_date_binder(date_from=None, offset=None, date_to=None):
    """Generate a binder for a certain date or range.

    date_from: start of date range.
    offset: length and direction of date range, negative ==
    in the past, unit is day.
    date_to: if offset is not provided, date_to designates
    end of time range. Default to date_from."""
    if date_from is None:
        date_from = str(date.today())
    if offset is None:
        if date_to is None:
            offset = 0
            date_to = date_from
    else:
        date_to = str((datetime.strptime(date_from, "%Y-%m-%d") + timedelta(days=offset)).date())
    result = Binder(name=date_from+'~'+date_to, kind='date')
    result.members = search_by_date(date_from, date_to)
    return result

def create_tag_binder(*tags):
    """Generate a binder containing only items with certain tags."""
    tag_array = []
    for tag in tags:
        tag_array.append(tag)
    result = Binder(name='tag: ' + str(tag_array), kind='tag')
    result.members = search_by_tag(tag_array)
    return result

def create_search_binder(*terms):
    """Generate a binder with items containing search terms."""
    conf = DBConfig()
    search_string = []
    for term in terms:
        search_string.append(term.lower())
    result = Binder(name='search: ' + str(search_string), kind='search')
    found = search(search_string)
    identity_rank = []
    for identity in found:
        rank = 0
        for term in terms:
            try:
                rank += conf.index_t.find_one({"identity": identity})['words'].index(term)
            except ValueError:
                rank += 0
        identity_rank.append((rank, identity))
    identity_rank.sort(reverse=True)
    result.members = []
    for _, identity in identity_rank:
        result.members.append(identity)
    return result
