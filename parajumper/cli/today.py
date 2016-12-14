"""Deal with 'today' command."""

import datetime
from clint.textui import puts, colored
from parajumper.db import create_date_binder, load_item

def show():
    """Show today's binder."""
    today = str(datetime.date.today())
    binder = create_date_binder(today)
    print(binder)
    items = []
    index = 0
    for member in binder.members:
        items.append(load_item(member))
    for item in items:
        puts(colored.blue("[%2d]" % index))
        print(item.__str__(verbose=0))
        index += 1
