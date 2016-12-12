"""fixtures and settings for tests on ParaJumper."""

import os
import pytest
from parajumper.config import Config
from parajumper.db import CLIENT

@pytest.fixture(scope="module")
def empty_config():
    """fixture function to delete existing config."""
    try:
        os.remove(os.environ['HOME'] + '/.config/parajumper/config.yaml')
        os.rmdir(os.environ['HOME'] + '/.config/parajumper/')
    except OSError:
        return

@pytest.fixture(scope='module')
def db_config():
    """Make db-related tests use test database."""
    conf = Config()
    conf.update_items({'database': {'db_name': 'test',
                                    'kind': 'mongodb',
                                    'location': 'mongodb://localhost:27017'}})
    print("Setting db to test")
    yield conf

@pytest.fixture()
def db_teardown():
    """Restore db to production env."""
    conf = Config()
    conf.update_items({'database': {'db_name': 'pj',
                                    'kind': 'mongodb',
                                    'location': 'mongodb://localhost:27017'}})
    print("Setting db to pj")
    yield conf

@pytest.fixture()
def empty_db():
    """empty test database."""
    database = CLIENT['test']
    items = database.items
    items.drop()
    binders = database.binders
    binders.drop()
    indices = database.indices
    indices.drop()
