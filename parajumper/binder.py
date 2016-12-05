"""Binders: collection of items."""

import uuid

BINDERS_DICT = dict()

def _print_members(items):
    if items == [] or items is None:
        return ''
    res = ''
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
        del(BINDERS_DICT[self.identity])
        del(self)
