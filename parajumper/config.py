"""
Process config file, which is a yaml file.

The default position of the file is at ~/.config/parajumper/config.yaml.

If the default file is not found, it falls back to ~/.config/parajumper/<any-name>.yaml.

If still nothing, a default config file is written.
"""
import os
import yaml

DEFAULT_CONFIG_PATH = os.environ['HOME'] + '/.config/parajumper'

CONF_DEFAULT = """author: Default ParaJumper
name: My ParaJumper Note
# This is default configuration for ParaJumper.
# Feel free to change it. """

def check_config():
    """Check if the config is available using os module."""
    try:
        os.listdir(DEFAULT_CONFIG_PATH)
    except OSError:
        os.mkdir(DEFAULT_CONFIG_PATH)
    try:
        conffile = open(DEFAULT_CONFIG_PATH + '/config.yaml')
    except OSError:
        conffile = open(DEFAULT_CONFIG_PATH + '/config.yaml', 'w+')
        print(CONF_DEFAULT, file=conffile)
    finally:
        conffile.close()
    return conffile.name

def read_config(f):
    """Read config into a dictionary.

    f: file name returned by check_config() or supplied in func call."""
    document = ''
    with open(f) as cf:
        for line in cf:
            document += line
    return yaml.load(document)
