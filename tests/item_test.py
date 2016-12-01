"""tests for the item module."""

import datetime
from parajumper.item import Item

def test_create_item(empty_db):
    """Test creation of item."""
    new_item = Item(bullet='.', content='# Test new item')
    assert new_item
    assert new_item.type == 'todo'
    assert new_item.content == '# Test new item'

def test_get_item_type(empty_db):
    """test if item type can be obtained correctly."""
    new_item = Item(content='# Test item')
    assert new_item.type == 'event'
    new_item = Item(bullet='19', content='Test')
    assert new_item.type == 'notes'

def test_update_item(empty_db):
    """test if items whose attributes are changed have different timestamp."""
    new_item = Item(bullet='.', content='Bring milk home')
    new_item.update(content='Bring peanuts home.')
    assert new_item.content == 'Bring peanuts home.'
    new_item.update(tags=['brown', 'white'])
    assert new_item.tags == ['brown', 'white']
    time1 = datetime.datetime.strptime(new_item.update_date, '%Y-%m-%d %H:%M:%S.%f')
    time2 = datetime.datetime.strptime(new_item.create_date, '%Y-%m-%d %H:%M:%S.%f')
    assert time1 - time2 > datetime.timedelta(0)

def test_unicode_content(empty_db):
    """Test if content unicode is handled correctly."""
    new_item = Item(bullet='o', content='你好お元気ですか')
    new_item.update(content=new_item.content[:2])
    assert new_item.content == '你好'
