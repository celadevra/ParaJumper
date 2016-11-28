"""fixtures and settings for tests on ParaJumper."""

import os
import pytest
from parajumper.config import Config

@pytest.fixture(scope="module")
def empty_config():
    """fixture function to delete existing config."""
    try:
        os.remove(os.environ['HOME'] + '/.config/parajumper/config.yaml')
        os.rmdir(os.environ['HOME'] + '/.config/parajumper/')
    except OSError:
        return
