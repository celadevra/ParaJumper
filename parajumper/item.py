"""
Module for handling Items.

Items are the basic meaningful units of notes in ParaJumper.

They can be created, updated, and removed.

They have attributes such as creation date, tags, types and contents.

The contents are Markdown text."""

from datetime import datetime
from parajumper.config import Config
from parajumper.db import CLIENT

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
        self.update_date = None
        self.identity = self.commit()

    def set_tags(self, *args):
        """Set the tags of self to the rest of the args."""
        all_tags = _process_tags(args)
        self.tags = all_tags
        self.update_date = str(datetime.now())
        self.identity = self.commit()

    def update(self, bullet=None, content=None, tags=None):
        """Change the calling item and update timestamp."""
        self.bullet = self.bullet if bullet is None else bullet
        self.type = _get_item_type(self.bullet)
        self.content = self.content if content is None else content
        self.tags = self.tags if tags is None else self.set_tags(tags)
        self.update_date = str(datetime.now())
        self.identity = self.commit()

    def commit(self):
        """Save item to database."""
        conf = Config()
        db_name = conf.options['database']['db_name']
        database = CLIENT[db_name]
        items = database.items
        try:
            identity = items.find_one({"_id": self.identity})['_id']
            items.update({"_id": identity}, self.__dict__)
        except AttributeError:
            identity = items.insert_one(self.__dict__).inserted_id
        return identity
