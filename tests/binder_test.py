"""Test for binder operations.
Binders are collections of items. In ParaJumper, all items from a day or a
longer time period forms a binder, so do all items with a certain tag, or
search result from a query."""

from parajumper.binder import Binder
import parajumper.db as db
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
    assert str(binder) == '%s binder: %s\n' % (binder.kind, binder.name)

def test_add_member():
    """Test for adding member(s) to binder."""
    binder = Binder()
    item = Item(bullet='1', content='# new member in the binder')
    item2 = Item(bullet='2', content='This is another paragraph.')
    id_item = db.save_item(item)
    id_item2 = db.save_item(item2)
    binder.add_members(id_item, id_item2)
    assert len(binder.members) == 2
    assert binder.members[1] == item2._id
