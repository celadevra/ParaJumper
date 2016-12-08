"""Test for binder operations.
Binders are collections of items. In ParaJumper, all items from a day or a
longer time period forms a binder, so do all items with a certain tag, or
search result from a query."""

from datetime import date, timedelta
import parajumper.db as db
from parajumper.binder import Binder, BINDERS_DICT, create_date_binder, create_tag_binder, create_search_binder
from parajumper.item import Item

def test_create_binder():
    """Test create method of binder class."""
    binder = Binder()
    assert binder.members is None
    assert binder.name == 'binder'
    assert binder.kind == 'adhoc'

def test_show_binder():
    """Test printing binder content."""
    binder = Binder()
    assert str(binder) == '%s binder: %s\n\n' % (binder.kind, binder.name)

def test_add_member():
    """Test for adding member(s) to binder."""
    binder = Binder()
    item = Item(bullet='1', content='# new member in the binder')
    item2 = Item(bullet='2', content='This is another paragraph.')
    binder.add_members(item, item2)
    assert len(binder.members) == 2
    assert binder.members[1] == item2.identity

def test_del_member():
    """Test for deleting members to binder."""
    binder = Binder()
    item = Item(bullet='1', content='# new member in the binder')
    item2 = Item(bullet='2', content='This is another paragraph.')
    binder.add_members(item, item2)
    assert binder.members == [item.identity, item2.identity]
    binder.del_members(item.identity)
    assert len(binder.members) == 1
    assert binder.members[0] == item2.identity

def test_members_are_unique():
    """Test for adding the same member to a binder again, the members
    list should not grow in this case."""
    binder = Binder()
    item = Item(bullet='1', content='# new member in the binder')
    item2 = Item(bullet='2', content='This is another paragraph.')
    binder.add_members(item, item2, item)
    assert len(binder.members) == 2

def test_remove_binder():
    """Test for removing binder from local env."""
    binder = Binder()
    length = len(BINDERS_DICT)
    assert BINDERS_DICT[binder.identity]
    binder.delete()
    assert len(BINDERS_DICT) == length - 1

def test_creating_binder_from_date(empty_db):
    """Test for creating binders from certain dates."""
    # 'today' binder, a default case
    item1 = Item(bullet='1', content='Test 1')
    item2 = Item(bullet='1', content='Test 2')
    db.save_item(item1)
    db.save_item(item2)
    binder = create_date_binder()
    assert item1.identity in binder.members
    assert item2.identity in binder.members
    # 'a week ago' binder, by setting
    item3 = Item(bullet='1', content='Test 3')
    item4 = Item(bullet='1', content='Test 4')
    item5 = Item(bullet='1', content='Test 5')
    item3.reschedule(str(date.today() - timedelta(days=6)))
    item4.reschedule(str(date.today() - timedelta(days=6)))
    db.save_item(item3)
    db.save_item(item4)
    db.save_item(item5)
    binder = create_date_binder(offset=-6)
    assert item3.identity in binder.members
    assert item4.identity in binder.members
    assert item5.identity in binder.members
    # 'from to' binder
    item6 = Item(bullet='1', content='Test 6')
    item7 = Item(bullet='1', content='Test 7')
    item6.reschedule(str(date.today() - timedelta(days=200)))
    item7.reschedule(str(date.today() + timedelta(days=203)))
    db.save_item(item6)
    db.save_item(item7)
    binder = create_date_binder(date_from=str(date.today() - timedelta(days=200)),
                                date_to=str(date.today() + timedelta(days=203)))
    assert item1.identity in binder.members
    assert item2.identity in binder.members
    assert item3.identity in binder.members
    assert item4.identity in binder.members
    assert item5.identity in binder.members
    assert item6.identity in binder.members
    assert item7.identity in binder.members

def test_creating_binder_from_tags(empty_db):
    """Test creating binder from items with the same tag."""
    item1 = Item(content="Test 1", tags=['history'])
    item2 = Item(content="Test 2", tags=['history', 'west'])
    item3 = Item(content="Test 3", tags=['geography', 'south'])
    item4 = Item(content="Test 3", tags=['history', 'south'])
    db.save_item(item1)
    db.save_item(item2)
    db.save_item(item3)
    db.save_item(item4)
    binder = create_tag_binder('history')
    assert item1.identity in binder.members
    assert item2.identity in binder.members
    assert item4.identity in binder.members
    assert item3.identity not in binder.members
    binder2 = create_tag_binder('south')
    assert item3.identity in binder2.members
    assert item4.identity in binder2.members
    assert item1.identity not in binder2.members
    binder3 = create_tag_binder('west', 'history')
    assert item2.identity in binder3.members

def test_creating_search_binder(empty_db):
    """Test creating binder from search term."""
    item1 = Item(content="竹外桃花三两枝")
    item2 = Item(content="春江水暖鸭先知")
    item3 = Item(content="蒌蒿满地芦芽短")
    item4 = Item(content="正是河豚欲上时")
    db.save_item(item1)
    db.save_item(item2)
    db.save_item(item3)
    db.save_item(item4)
    binder = create_search_binder("桃花")
    assert item1.identity in binder.members
    assert item2.identity not in binder.members
    assert len(binder.members) == 1
    item5 = Item(content="# Epigraph\nProgramming is the activity of...")
    item6 = Item(content="# Epigraph\nProgramming is not the activity of...")
    item7 = Item(content="# Epigraph\nStatistics is the activity of ...")
    item8 = Item(content="# Epigraph\nStatistics is not the activity of ...")
    db.save_item(item5)
    db.save_item(item6)
    db.save_item(item7)
    db.save_item(item8)
    binder2 = create_search_binder('activity')
    assert len(binder2.members) == 4
    binder3 = create_search_binder('programming')
    assert len(binder3.members) == 2
    assert item5.identity in binder3.members
    assert item6.identity in binder3.members
