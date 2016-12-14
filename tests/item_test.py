"""tests for the item module."""

import datetime
from parajumper.item import Item, ITEMS_DICT
from parajumper.config import Config

def test_create_item():
    """Test creation of item."""
    new_item = Item(bullet='.', content='# Test new item')
    assert new_item
    assert new_item.kind == 'todo'
    assert new_item.content == '# Test new item'

def test_get_item_kind():
    """test if item kind can be obtained correctly."""
    new_item = Item(content='# Test item')
    assert new_item.kind == 'event'
    new_item = Item(bullet='19', content='Test')
    assert new_item.kind == 'notes'

def test_show_item():
    """test item printing."""
    new_item = Item(content="Content.", bullet="*")
    assert str(new_item) == "* Content.\ntags: []\nScheduled: %s by %s\n" % (str(datetime.date.today()), new_item.author)

def test_show_item_details():
    """test showing item with all its relevant information."""
    conf = Config()
    new_item = Item(bullet='.', content='Milk', tags='grocery')
    assert new_item.show_detail() == ". (%s) Milk\n  grocery\n  S: %s  BY: %s\n  id: %s\n" % (new_item.kind, str(datetime.date.today()), conf.options['author'], new_item.identity)

def test_update_item():
    """test if items whose attributes are changed have different timestamp."""
    new_item = Item(bullet='.', content='Bring milk home')
    new_item.update(content='Bring peanuts home.')
    assert new_item.content == 'Bring peanuts home.'
    new_item.update(tags=['brown', 'white'])
    assert new_item.tags == ['brown', 'white']

def test_reschedule_item():
    """Test if items can be correctly rescheduled."""
    new_item = Item(bullet='o', content='Castro died.')
    assert new_item.schedule == str(datetime.date.today())
    new_item.reschedule('2016-12-02')
    assert new_item.schedule == '2016-12-02'

def test_unicode_content():
    """Test if content unicode is handled correctly."""
    new_item = Item(bullet='o', content='你好お元気ですか')
    new_item.update(content=new_item.content[:2])
    assert new_item.content == '你好'

def test_processing_tags():
    """Test various tags input and the resulting item."""
    new_item1 = Item(tags=['grocery'])
    new_item2 = Item(tags='produce')
    new_item3 = Item(tags=['brown', 'white'])
    new_item4 = Item(tags={'green': '1', 'blue': 2})
    assert new_item1.tags == ['grocery']
    assert new_item2.tags == ['produce']
    assert new_item3.tags == ['brown', 'white']
    assert new_item4.tags == ['blue', 'green']

def test_delete_item():
    """Test removing item from dict."""
    new_item = Item()
    identity = new_item.identity
    assert ITEMS_DICT[new_item.identity].content == ''
    new_item.delete()
    assert identity not in ITEMS_DICT.keys()
