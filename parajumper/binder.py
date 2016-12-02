"""Binders: collection of items."""

import parajumper.db as db

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

    def __str__(self):
        """Text representation of binder."""
        return "%s binder: %s\n%s" % (self.kind, self.name, _print_members(self.members))

    def add_members(self, *args):
        """add items to binder. Implicitly save item to db if item hasn't 
        been saved.

        args: Item objects."""
        if self.members is None:
            self.members = []
        for arg in args:
            if hasattr(arg, '_id'):
                self.members.append(arg._id)
            else:
                identity = db.save_item(arg)
                self.members.append(identity)
