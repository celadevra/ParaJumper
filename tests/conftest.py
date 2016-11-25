"""fixtures and settings for tests on ParaJumper."""

import os
import pytest
from parajumper import config

@pytest.fixture(scope="module")
def empty_config():
    """fixture function to delete existing config."""
    try:
        os.remove(os.environ['HOME'] + '/.config/parajumper/config.yaml')
        os.rmdir(os.environ['HOME'] + '/.config/parajumper/')
    except OSError:
        return

@pytest.fixture(scope="module")
def create_config():
    """fixture function to create default config."""
    if not os.access(os.environ['HOME'] + '/.config/parajumper/config.yaml', os.R_OK):
        config.check_config()
    return
