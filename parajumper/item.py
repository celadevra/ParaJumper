"""
Module for handling Items.

Items are the basic meaningful units of notes in ParaJumper.

They can be created, updated, and removed.

They have attributes such as creation date, tags, types and contents.

The contents are Markdown text."""

from datetime import datetime
from parajumper.config import Config

def _get_item_type(bullet):
    """Obtain/Set item type from config and bullets.

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

class Item():
    """Items: individual notes or snippets.

    attributes:
    - create_date
    - update_date
    - tags
    - type
    - content
    - identity
    - rev

    methods:
    - __init__: create item C
    - __str__: show item R
    - update: update item U

    helpers:
    - _get_item_type: from bullet
    - _process_tags
    """

    def __init__(self, bullet='o', content=None, tags=None):
        """Init item with the help of get_item_type()."""
        self.bullet = bullet
        self.content = "" if content is None else content
        self.create_date = str(datetime.now())
        self.tags = [] if tags is None else tags
        self.type = _get_item_type(bullet)
        self.update_date = None

    def __str__(self):
        """Show item in text format."""
        return "%s %s\ntags: %s\nCreated: %s\nUpdated: %s" % (
            self.bullet,
            self.content, self.tags,
            self.create_date.split()[0],
            self.update_date.split()[0] if self.update_date is not None else 'N/A')

    def update(self, bullet=None, content=None, tags=None):
        """Change the calling item and update timestamp."""
        self.bullet = self.bullet if bullet is None else bullet
        self.type = _get_item_type(self.bullet)
        self.content = self.content if content is None else content
        self.tags = self.tags if tags is None else _process_tags(tags)
        self.update_date = str(datetime.now())
