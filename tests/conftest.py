"""fixtures and settings for tests on ParaJumper."""

import os
import pytest
from parajumper.config import Config, DBConfig

@pytest.fixture(scope="module")
def empty_config():
    """fixture function to delete existing config."""
    try:
        os.remove(os.environ['HOME'] + '/.config/parajumper/config.yaml')
        os.rmdir(os.environ['HOME'] + '/.config/parajumper/')
    except OSError:
        return

@pytest.fixture(scope='module', autouse=True)
def set_up():
    """Make db-related tests use test database."""
    conf = Config()
    conf.update_items({'database': {'db_name': 'test',
                                    'kind': 'mongodb',
                                    'location': 'mongodb://localhost:27017'}})
    print("Setting db to test")
    yield conf
    Config()
    conf.update_items({'database': {'db_name': 'pj',
                                    'kind': 'mongodb',
                                    'location': 'mongodb://localhost:27017'}})
    print("Setting db to pj")

@pytest.fixture()
def empty_db():
    """empty test database."""
    conf = DBConfig()
    conf.item_t.drop()
    conf.binder_t.drop()
    conf.index_t.drop()
