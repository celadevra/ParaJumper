"""fixtures and settings for tests on ParaJumper."""

import os
import pytest
from parajumper.db import CLIENT

@pytest.fixture(scope="module")
def empty_config():
    """fixture function to delete existing config."""
    try:
        os.remove(os.environ['HOME'] + '/.config/parajumper/config.yaml')
        os.rmdir(os.environ['HOME'] + '/.config/parajumper/')
    except OSError:
        return

@pytest.fixture(scope="module")
def empty_db():
    """empty test database."""
    database = CLIENT.pj
    items = database.items
    items.drop()
    binders = database.binders
    binders.drop()
