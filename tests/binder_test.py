"""Test for binder operations.
Binders are collections of items. In ParaJumper, all items from a day or a
longer time period forms a binder, so do all items with a certain tag, or
search result from a query."""

from parajumper.binder import Binder

def test_create_binder():
    """Test create method of binder class."""
    binder = Binder()
    assert binder.members is None
