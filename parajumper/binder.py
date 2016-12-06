"""Binders: collection of items."""

import uuid
from datetime import date, datetime, timedelta
import parajumper.db

BINDERS_DICT = dict()

def _print_members(items):
    if items == [] or items is None:
        return ''
    res = ''
    #TODO: insert index of items as well
    for item in items:
        res += str(item) + '\n\n'
    res = res[:-2] # remove trailing \n
    return res

class Binder():
    """Binder class. A binder has multiple items as its member, and can
    specify the order of these members. A collection can be created, read,
    updated (add/delete member), or deleted (without deleting the member).

    attributes:
    - name
    - kind: date, search, tag, adhoc
    - members: a list of items in the binder
    - identity

    methods:
    - __init__ C
    - __str__ R
    - add_members U
    - remove_members U
    - delete D"""

    def __init__(self, name='binder', kind='adhoc', members=None):
        """Create a binder."""
        self.name = name
        self.kind = kind
        self.members = members
        self.identity = str(uuid.uuid4())
        BINDERS_DICT[self.identity] = self

    def __str__(self):
        """Text representation of binder."""
        return "%s binder: %s\n%s\n" % (self.kind, self.name, _print_members(self.members))

    def add_members(self, *items):
        """add items to binder.

        args: Item objects."""
        if self.members is None:
            self.members = []
        for item in items:
            if item.identity not in self.members:
                self.members.append(item.identity)

    def del_members(self, *ids):
        """delete items from binder but not from db.

        args: Item ids."""
        for iden in ids:
            self.members.remove(iden)

    def delete(self):
        """Delete binder from the local env."""
        del BINDERS_DICT[self.identity]
        del self

# outside of binder class
def create_date_binder(date_from=None, offset=None, date_to=None):
    """Generate a binder for a certain date or range.

    date_from: start of date range.
    offset: length and direction of date range, negative ==
    in the past, unit is day.
    date_to: if offset is not provided, date_to designates
    end of time range. Default to date_from."""
    if date_from is None:
        date_from = str(date.today())
    if offset is None:
        if date_to is None:
            offset = 0
            date_to = date_from
    else:
        date_to = str((datetime.strptime(date_from, "%Y-%m-%d") + timedelta(days=offset)).date())
    result = Binder(name=date_from+'~'+date_to, kind='date')
    result.members = parajumper.db.search_by_date(date_from, date_to)
    return result
