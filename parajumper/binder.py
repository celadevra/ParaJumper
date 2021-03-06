"""Binders: collection of items."""

import uuid
from random import shuffle
from clint.textui import colored

BINDERS_DICT = dict()

def _print_members(items):
    if items == [] or items is None:
        return ''
    res = ''
    index = 0
    for item in items:
        res += '[' + str(index) + ']\n' + str(item) + '\n\n'
        index += 1
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
    - reorder U
    - rename U
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
        return "%s binder: %s\n" % (colored.green(self.kind), colored.yellow(self.name))

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

    def shuffle_members(self):
        """shuffle order of members"""
        shuffle(self.members)

    def rename(self, new_name):
        """Rename binder. If binder is adhoc, just rename. Else, set the
        binder kind to adhoc then rename."""
        if self.kind == 'adhoc':
            self.name = new_name
        else:
            self.kind = 'adhoc'
            self.name = new_name

    def reorder(self, from_index, to_index):
        """Reorder items in a binder by moving one item from
        from_index to to_index."""
        order = list(range(len(self.members)))
        del order[from_index]
        order.insert(to_index, from_index)
        self.members = [self.members[i] for i in order]

    def delete(self):
        """Delete binder from the local env."""
        del BINDERS_DICT[self.identity]
        del self
