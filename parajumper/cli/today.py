"""Deal with 'day' command."""

import datetime
from clint.textui import puts, colored
from parajumper.db import create_date_binder, load_item

def dispatch(args):
    """Dispatch and control command behaviours according to args."""
    v_level = 0
    if '-v' in args.flags:
        v_level = 1
    if '-vv' in args.flags:
        v_level = 2
    if '-vvv' in args.flags:
        v_level = 3
    return show(v_level)

def show(level=0, today=True, date_from=None, date_to=None, ago=None):
    """Show today's binder."""
    if today:
        today = str(datetime.date.today())
        binder = create_date_binder(today)
    print(binder)
    items = []
    index = 0
    for member in binder.members:
        items.append(load_item(member))
    for item in items:
        puts(colored.blue("[%2d]" % index))
        print(item.__str__(verbose=level))
        index += 1
