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

def test_set_tags():
    """test if tags can be set correctly."""
    new_item = Item(bullet='3', content='测试')
    assert new_item.tags == []
    new_item.set_tags('play', 'test')
    assert new_item.tags == ['play', 'test']
    new_item.set_tags(['foo', 'bar'])
    assert new_item.tags == ['bar', 'foo']
    new_item.set_tags({'a':1, 'b':2})
    assert new_item.tags == ['a', 'b']
    new_item.set_tags(135, '246')
    assert new_item.tags == ['135', '246']
    new_item.set_tags((50, 21))
    assert new_item.tags == ['21', '50']
#TODO: test for unicode cases
