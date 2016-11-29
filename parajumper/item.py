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

class Item():
    """Items: individual notes or snippets.

    attributes:
    - create_date
    - update_date
    - tags
    - type
    - content

    methods:
    - __init__: create item

    helpers:
    - get_item_type: from bullet
    """

    def __init__(self, bullet='o', content=None, tags=None):
        """Init item with the help of get_item_type()."""
        self.bullet = bullet
        self.content = "" if content is None else content
        self.create_date = str(datetime.now())
        self.tags = [] if tags is None else tags
        self.type = _get_item_type(bullet)
