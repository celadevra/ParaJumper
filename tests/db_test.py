"""Tests for database operations."""
from parajumper.item import Item
from parajumper.binder import Binder
import parajumper.db as db

def test_save_item(empty_db):
    """Test for saving item."""
    item = Item(content="Test content", bullet=".", tags=['oper'])
    db.save_item(item)
    assert db.ITEM_T.find_one({"content":"Test content"})['tags'] == ['oper'] is not None

def test_load_item(empty_db):
    """Test for loading item."""
    item = Item(content="Test content", bullet=".", tags=['oper'])
    identity = db.save_item(item)
    item2 = db.load_item(identity)
    assert item.__dict__ == item2.__dict__

def test_removing_item(empty_db):
    """Test for removing item."""
    item = Item(content="Test content", bullet=".", tags=['oper'])
    identity = db.save_item(item)
    db.remove_item(identity)
    assert db.ITEM_T.find_one({"identity": identity}) is None

def test_save_binder_and_members(empty_db):
    """Test for saving binder and its members. Items not in the
    binder should not be saved."""
    item1 = Item(content="I'm in a binder.")
    item2 = Item(content="Not in a binder.")
    binder = Binder()
    binder.add_members(item1)
    identity = db.save_binder(binder)
    assert db.ITEM_T.find_one({"content":"I'm in a binder."}) is not None
    assert db.BINDER_T.find_one({"identity":identity}) is not None
    assert db.ITEM_T.find_one({"content":item2.content}) is None

def test_removing_binder(empty_db):
    """Test for removing binder from db. Items in the binder will be reserved."""
    item1 = Item(content="This is test of 12-03")
    binder = Binder()
    binder.add_members(item1)
    item_identity = db.save_item(item1)
    binder_identity = db.save_binder(binder)
    db.remove_binder(binder_identity)
    assert db.BINDER_T.find_one({"identity": binder_identity}) is None
    assert db.ITEM_T.find_one({"identity": item_identity})
