"""Deal with 'day' command."""

import datetime
from clint.textui import puts, colored
from parajumper.db import create_date_binder, load_item

def dispatch(args):
    """Dispatch and control command behaviours according to args."""
    v_level = 0
    date_to = None
    date_from = None
    ago = None
    today = True
    if '-v' in args.flags:
        v_level = 1
    if '-vv' in args.flags:
        v_level = 2
    if '-vvv' in args.flags:
        v_level = 3
    if '-df' in args.flags:
        date_from = args.value_after('-df')
        today = False
    if '-dt' in args.flags:
        date_to = args.value_after('-dt')
        today = False
    if '-da' in args.flags:
        ago = args.value_after('-da')
        today = False
    return show(v_level, today, date_from, date_to, ago)

def show(level=0, today=True, date_from=None, date_to=None, ago=None):
    """Show today's binder."""
    if today:
        today = str(datetime.date.today())
        binder = create_date_binder(today)
    if (date_from is not None) or (date_to is not None):
        if ago is not None:
            binder = create_date_binder(date_from=date_from, offset=int(ago), date_to=date_to)
        else:
            binder = create_date_binder(date_from=date_from, offset=None, date_to=date_to)
    print(binder)
    items = []
    index = 0
    for member in binder.members:
        items.append(load_item(member))
    for item in items:
        puts(colored.blue("[%2d]" % index))
        print(item.__str__(verbose=level))
        index += 1
