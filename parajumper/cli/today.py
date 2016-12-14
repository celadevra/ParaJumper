"""Deal with 'today' command."""

import datetime
from parajumper.db import create_date_binder

def show():
    """Show today's binder."""
    today = str(datetime.date.today())
    binder = create_date_binder(today)
    print(binder)
