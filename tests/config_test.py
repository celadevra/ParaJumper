"""
Tests for config module
"""

import os
from parajumper.config import Config

CONF_FILE = os.environ['HOME'] + '/.config/parajumper/config.yaml'

def test_config_creation(empty_config):
    """test if config can be created when absent"""
    assert not os.access(CONF_FILE, os.F_OK)
    Config()
    assert os.access(CONF_FILE, os.R_OK)

def test_config_content():
    """test if config's content is the expected default content."""
    line_count = 0
    word = ''
    with open(CONF_FILE) as f:
        for line in f:
            line_count += 1
            if line_count == 1:
                word = line.split()[0]
    assert line_count == 4
    assert word == 'author:'

def test_read_config():
    """test if the config is read correctly."""
    conf = Config()
    conf.update_config(CONF_FILE)
    assert conf['author'] == 'Default ParaJumper'
    assert conf['name'] == 'My ParaJumper Note'

# next: insert dict into config file as adding new config
def test_add_config():
    """test inserting new items into the config."""
    conf = Config()
    conf.update_items({'foo': 'bar'})
    assert conf['foo'] == 'bar'
