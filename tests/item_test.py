"""tests for the item module."""

from parajumper.item import Item

def test_create_item():
    """Test creation of item."""
    new_item = Item(bullet='.', content='# Test new item')
    assert new_item
    assert new_item.type == 'todo'
    assert new_item.content == '# Test new item'

def test_get_item_type():
    """test if item type can be obtained correctly."""
    new_item = Item(content='# Test item')
    assert new_item.type == 'event'
    new_item = Item(bullet='19', content='Test')
    assert new_item.type == 'notes'
