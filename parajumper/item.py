"""
Module for handling Items.

Items are the basic meaningful units of notes in ParaJumper.

They can be created, updated, and removed.

They have attributes such as creation date, tags, types and contents.

The contents are Markdown text."""

import uuid
import re
from datetime import date
from parajumper.config import Config

ITEMS_DICT = dict()

def _get_item_kind(bullet):
    """Obtain/Set item kind from config and bullets.

    bullet: a character"""
    conf = Config()
    try:
        if isinstance(int(bullet), int):
            return 'notes' # numbered bullets are notes
    except ValueError:
        pass
    bullet_table = conf.options['bullets']
    bullet_dict = dict()
    for elem in bullet_table:
        pair = elem.popitem()
        bullet_dict[pair[0]] = pair[1]
    return bullet_dict.get(bullet, 'default')

def _process_tags(args):
    """flatten input, and return a list of all tags, sorted."""
    if isinstance(args, str):
        return [args]
    result = []
    for arg in args:
        if isinstance(arg, list):
            result += _process_tags(arg)
        elif isinstance(arg, tuple):
            result += _process_tags(list(arg))
        elif isinstance(arg, dict):
            result += _process_tags(arg.keys())
        elif isinstance(arg, str):
            result.append(arg)
        else:
            result.append(str(arg))
    result.sort()
    return result

def _show_tags(tags):
    """Show tags as a series of words/phrases, separated by colons."""
    res = ""
    if len(tags) == 0:
        return "[]"
    else:
        for tag in tags:
            res = res + tag + ':'
    return res[:-1]

class Item():
    """Items: individual notes or snippets.

    attributes:
    - schedule
    - tags
    - type
    - content
    - identity
    - author

    methods:
    - __init__: create item C
    - __str__: show item R
    - update: update item U
    - remove: remove item from dict D

    helpers:
    - _get_item_type: from bullet
    - _process_tags
    - _show_tags
    """

    def __init__(self, bullet='o', content=None, tags=None):
        """Init item with the help of get_item_type().

        bullet: the leading character before the paragraph, determines
        the type of the entry.
        content: content of the paragraph.
        tags: tags."""
        conf = Config()
        self.author = conf.options['author']
        self.bullet = bullet
        self.content = "" if content is None else content
        self.schedule = str(date.today())
        self.tags = [] if tags is None else _process_tags(tags)
        self.kind = _get_item_kind(bullet)
        self.identity = str(uuid.uuid4())
        ITEMS_DICT[self.identity] = self

    def __str__(self):
        """Show item in text format."""
        return "%s %s\ntags: %s\nScheduled: %s by %s\n" % (
            self.bullet,
            self.content, _show_tags(self.tags),
            self.schedule, self.author)

    def show_detail(self):
        """Show item in text format, more detailed than __str__. Mainly
        for debugging"""
        return "%s %s\ntags: %s\nScheduled: %s by %s\nkind: %s\nid: %s\n" % (
            self.bullet,
            self.content,
            _show_tags(self.tags),
            self.schedule,
            self.author,
            self.kind,
            self.identity)

    def update(self, bullet=None, content=None, tags=None):
        """Change the calling item and update timestamp."""
        self.bullet = self.bullet if bullet is None else bullet
        self.kind = _get_item_kind(self.bullet)
        self.content = self.content if content is None else content
        self.tags = self.tags if tags is None else _process_tags(tags)

    def reschedule(self, date_string):
        """Change the scheduled date of the item."""
        date_re = re.compile(r'^[0-9]{4}-(0[0-9]|1[0-2])-([0-2][0-9]|3[01])$')
        if date_re.match(date_string) is None:
            raise ValueError
        else:
            self.schedule = date_string

    def delete(self):
        """Remove item from dict."""
        ITEMS_DICT.pop(self.identity)
        del self
