"""Test for binder operations.
Binders are collections of items. In ParaJumper, all items from a day or a
longer time period forms a binder, so do all items with a certain tag, or
search result from a query."""

from parajumper.binder import Binder
import parajumper.db as db

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
