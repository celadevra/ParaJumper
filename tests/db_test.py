"""Tests for database operations."""
from parajumper.item import Item
import parajumper.db as db

def test_save_item(empty_db):
    """Test for saving item."""
    item = Item(content="Test content", bullet=".", tags=['oper'])
    db.save_item(item)
    assert db.ITEM_T.find_one({"content":"Test content"})['tags'] == ['oper']

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
