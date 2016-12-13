"""Tests for database operations."""
from parajumper.item import Item, ITEMS_DICT
from parajumper.binder import Binder, BINDERS_DICT
from parajumper.config import DBConfig
import parajumper.db as db

def test_save_item(empty_db):
    """Test for saving item."""
    conf = DBConfig()
    item = Item(content="Test content", bullet=".", tags=['oper'])
    db.save_item(item)
    assert conf.item_t.find_one({"content":"Test content"})['tags'] == ['oper'] is not None

def test_load_item(empty_db):
    """Test for loading item."""
    item = Item(content="Test content", bullet=".", tags=['oper'])
    identity = db.save_item(item)
    item2 = db.load_item(identity)
    assert item.__dict__ == item2.__dict__
    assert ITEMS_DICT[identity] == item2

def test_removing_item(empty_db):
    """Test for removing item."""
    conf = DBConfig()
    item = Item(content="Test content", bullet=".", tags=['oper'])
    identity = db.save_item(item)
    db.remove_item(identity)
    assert conf.item_t.find_one({"identity": identity}) is None

def test_save_binder_and_members(empty_db):
    """Test for saving binder and its members. Items not in the
    binder should not be saved."""
    conf = DBConfig()
    item1 = Item(content="I'm in a binder.")
    item2 = Item(content="Not in a binder.")
    binder = Binder()
    binder.add_members(item1)
    identity = db.save_binder(binder)
    assert conf.item_t.find_one({"content":"I'm in a binder."}) is not None
    assert conf.binder_t.find_one({"identity":identity}) is not None
    assert conf.item_t.find_one({"content":item2.content}) is None

def test_removing_binder(empty_db):
    """Test for removing binder from db. Items in the binder will be reserved."""
    conf = DBConfig()
    item1 = Item(content="This is test of 12-03")
    binder = Binder()
    binder.add_members(item1)
    item_identity = db.save_item(item1)
    binder_identity = db.save_binder(binder)
    db.remove_binder(binder_identity)
    assert conf.binder_t.find_one({"identity": binder_identity}) is None
    assert conf.item_t.find_one({"identity": item_identity})

def test_loading_binder(empty_db):
    """Test for loading binder from db."""
    binder = Binder()
    identity = db.save_binder(binder)
    assert BINDERS_DICT[identity] == binder
    binder.delete()
    assert not identity in BINDERS_DICT.keys()
    binder = db.load_binder(identity)
    assert BINDERS_DICT[identity] == binder

def test_indices_order(empty_db):
    """Test if indices are ordered by frequency."""
    conf = DBConfig()
    item1 = Item(content="Do you call this this and that also this?")
    db.save_item(item1)
    wordlist = conf.index_t.find_one({"identity":item1.identity})['words']
    assert wordlist[-1] == 'this'
