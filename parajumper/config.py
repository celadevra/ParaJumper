"""
Process config file, which is a yaml file.

The default position of the file is at ~/.config/parajumper/config.yaml.

If the default file is not found, it falls back to a filename supplied at the
init of config class.

If the file does not exist, a default config file is written.
"""
import os
from ruamel import yaml

DEFAULT_CONFIG_FILE = os.environ['HOME'] + '/.config/parajumper/config.yaml'

CONF_DEFAULT = """author: Default ParaJumper
name: My ParaJumper Note
# This is default configuration for ParaJumper.
# See documents for possible options and values. """

class Config():
    """configurations for ParaJumper

    attributes:
        - options: dictionary of config item and their values.
    methods:
        - __init__
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
            self.options = yaml.load(document)

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
        new_conf = yaml.load(document)
        self.options.update(new_conf)
        conf_file = open(write_f, 'w')
        yaml.dump(self.options, conf_file, default_flow_style=False)
        conf_file.close()

    def update_items(self, dict_conf_item, conf_f=DEFAULT_CONFIG_FILE):
        """add/change items in the config.

        dict_conf_item: a dict recording things to be added/changed in the conf.
        conf_f: file to write config to."""
        self.options.update(dict_conf_item)
        conf_file = open(conf_f, 'w+')
        yaml.dump(self.options, conf_file, default_flow_style=False)
        conf_file.close()

    def remove(self, k, conf_f=DEFAULT_CONFIG_FILE):
        """remove specified key and its value from conf dict.

        k: key to remove.
        conf_f: file to write config to."""
        del self.options[k]
        conf_file = open(conf_f, 'w+')
        yaml.dump(self.options, conf_file, default_flow_style=False)
        conf_file.close()
