"""
Tests for config module
"""

import os
from parajumper.config import Config

CONF_FILE = os.environ['HOME'] + '/.config/parajumper/config.yaml'

def test_config_creation(empty_config):
    """test if config can be created when absent"""
    assert not os.access(CONF_FILE, os.F_OK)
    conf = Config()
    assert os.access(CONF_FILE, os.R_OK)
    assert conf.options['author'] == 'Default ParaJumper'

def test_config_content():
    """test if config's content is the expected default content."""
    line_count = 0
    word = ''
    Config()
    with open(CONF_FILE) as conf:
        for line in conf:
            line_count += 1
            if line_count == 1:
                word = line.split()[0]
    assert line_count == 17
    assert word == 'author:'

def test_read_config():
    """test if the config is read correctly."""
    conf = Config()
    conf.update_config(CONF_FILE)
    assert conf.options['author'] == 'Default ParaJumper'
    assert conf.options['name'] == 'My ParaJumper Note'

def test_save_config():
    """test if the config is sync with file."""
    Config()
    assert os.access(CONF_FILE, os.R_OK)
    lines = []
    with open(CONF_FILE) as conf_file:
        for line in conf_file:
            lines.append(line)
    assert lines[0].split()[0] == 'author:'

def test_add_config():
    """test inserting new items into the config."""
    conf = Config()
    conf.update_items({'foo': 'bar'})
    assert conf.options['foo'] == 'bar'

def test_remove_config():
    """test removing config."""
    conf = Config()
    conf.update_items({'foo': 'bar'})
    conf.remove('foo')
    assert not 'foo' in conf.options.keys()
