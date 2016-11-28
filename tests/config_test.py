"""
Tests for config module
"""

import os
from parajumper import config

CONF_FILE = os.environ['HOME'] + '/.config/parajumper/config.yaml'

def test_config_creation(empty_config):
    """test if config can be created when absent"""
    assert not os.access(CONF_FILE, os.F_OK)
    config.check_config()
    assert os.access(CONF_FILE, os.R_OK)

def test_config_content(create_config):
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

def test_read_config(create_config):
    """test if the config is read correctly."""
    conf = config.read_config(CONF_FILE)
    assert conf['author'] == 'Default ParaJumper'
    assert conf['name'] == 'My ParaJumper Note'

# next: insert dict into config file as adding new config
def test_add_config(create_config):
    """test inserting new items into the config."""
    config.add_config(CONF_FILE, {'foo': 'bar'})
    conf = config.read_config(CONF_FILE)
    assert conf['foo'] == 'bar'
