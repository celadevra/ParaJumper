"""
Tests for config module
"""

import os
import pytest
from parajumper import config

def test_config_creation(empty_config):
    """test if config can be created when absent"""
    assert not os.access(os.environ['HOME'] + '/.config/parajumper/config.yaml', os.F_OK)
    config.check_config()
    assert os.access(os.environ['HOME'] + '/.config/parajumper/config.yaml', os.R_OK)

def test_config_content(create_config):
    """test if config's content is the expected default content."""
    line_count = 0
    word = ''
    with open(os.environ['HOME'] + '/.config/parajumper/config.yaml') as f:
        for line in f:
            line_count += 1
            if line_count == 2:
               word = line.split()[0] 
    assert line_count == 6
    assert word == 'author:'
    
