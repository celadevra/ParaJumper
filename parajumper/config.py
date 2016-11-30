"""
Process config file, which is a yaml file.

The default position of the file is at ~/.config/parajumper/config.yaml.

If the default file is not found, it falls back to a filename supplied at the
init of config class.

If the file does not exist, a default config file is written.
"""
import os
import ruamel
from ruamel import yaml

DEFAULT_CONFIG_FILE = os.environ['HOME'] + '/.config/parajumper/config.yaml'

CONF_DEFAULT = """author: Default ParaJumper
name: My ParaJumper Note
bullets:
    - '.': todo
    - 'o': event
    - '1': notes
database:
#    - kind: sqlite
#    - location: ~/.local/share/parajumper/notes.db
    - kind: couchdb
    - location: 'localhost:5984/'
    - db_name: pj
    - user: pj
    - password: pj
# This is default configuration for ParaJumper.
# See documents for possible options and values.
# Recommended way to change config is through CLI."""

class Config():
    """configurations for ParaJumper

    attributes:
        - options: dictionary of config item and their values.
    methods:
        - __init__
        - save: save config to file, used by methods below.
        - update_config: read additional settings from another file
        - update_items: change individual settings
        - remove: delete a key/value pair from config"""

    def __init__(self, f=DEFAULT_CONFIG_FILE):
        """Check if the config is available using os module.
        If the file is present, read the config into a dict,
        if not, create the file with default, and read it into a dict.
        Return the dict.

        f: config file to read."""
        try:
            os.listdir(os.path.dirname(f))
        except OSError:
            os.mkdir(os.path.dirname(f))
        try:
            conffile = open(f)
        except OSError:
            conffile = open(f, 'w+')
            conffile.write(CONF_DEFAULT)
            conffile.close()
            conffile = open(f)
        finally:
            document = ''
            for line in conffile:
                document += line
            self.options = yaml.load(document, Loader=ruamel.yaml.Loader)

    def save(self, dest_f=DEFAULT_CONFIG_FILE):
        """Save config to a file.

        dest_f: path to file."""
        comments = """
        # This is default configuration for ParaJumper.
        # See documents for possible options and values.
        # Recommended way to change config is through CLI."""
        save_to = open(dest_f, 'w+')
        yaml.dump(self.options, save_to, default_flow_style=False)
        save_to.write(comments)
        save_to.close()

    def update_config(self, read_f=DEFAULT_CONFIG_FILE, write_f=DEFAULT_CONFIG_FILE):
        """Read config from a file into a dictionary.
        Then merge it with the existing directory.

        read_f: file name returned by check_config() or supplied in func call.
        write_f: config file to write to."""
        document = ''
        conf_file = open(read_f)
        for line in conf_file:
            document += line
        conf_file.close()
        new_conf = yaml.load(document, Loader=ruamel.yaml.Loader)
        self.options.update(new_conf)
        self.save(write_f)

    def update_items(self, dict_conf_item, conf_f=DEFAULT_CONFIG_FILE):
        """add/change items in the config.

        dict_conf_item: a dict recording things to be added/changed in the conf.
        conf_f: file to write config to."""
        self.options.update(dict_conf_item)
        self.save(conf_f)

    def remove(self, k, conf_f=DEFAULT_CONFIG_FILE):
        """remove specified key and its value from conf dict.

        k: key to remove.
        conf_f: file to write config to."""
        del self.options[k]
        self.save(conf_f)
    # TODO: need a method to quickly add new item type (bullets)
