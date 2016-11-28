"""
Process config file, which is a yaml file.

The default position of the file is at ~/.config/parajumper/config.yaml.

If the default file is not found, it falls back to a filename supplied at the
init of config class.

If the file does not exist, a default config file is written.
"""
import os
import yaml

DEFAULT_CONFIG_FILE = os.environ['HOME'] + '/.config/parajumper/config.yaml'

CONF_DEFAULT = """author: Default ParaJumper
name: My ParaJumper Note
# This is default configuration for ParaJumper.
# Feel free to change it. """

class Config(dict):
    """configurations for ParaJumper"""

    def __init__(self, f=DEFAULT_CONFIG_FILE):
        """Check if the config is available using os module.
        If the file is present, read the config into a dict,
        if not, create the file with default, and read it into a dict.
        Return the dict."""
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
            document = ""
            for line in conffile:
                document += line
            self = yaml.load(document)

    def update_config(self, f=DEFAULT_CONFIG_FILE, df=DEFAULT_CONFIG_FILE):
        """Read config from a file into a dictionary.
        Then merge it with the existing directory.

        f: file name returned by check_config() or supplied in func call.
        df: config file to write to."""
        document = ''
        cf = open(f)
        for line in cf:
            document += line
        cf.close()
        new_conf = yaml.load(document)
        self.update(new_conf)
        cf = open(df, 'w')
        yaml.dump(self, cf)
        cf.close()

    def update_items(self, d={}, f=DEFAULT_CONFIG_FILE):
        """add/change items in the config.

        d: a dict recording things to be added/changed in the conf.
        f: file to write config to."""
        self.update(d)
        cf = open(f, 'w+')
        yaml.dump(self, cf)
        cf.close()

    def remove(self, k, f=DEFAULT_CONFIG_FILE):
        """remove specified key and its value from conf dict.

        k: key to remove.
        f: file to write config to."""
        del(self[k])
        cf = open(f, 'w+')
        yaml.dump(self, cf)
        cf.close()
