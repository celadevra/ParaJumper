"""Deal with 'day' command."""

import datetime
import tempfile
import os
from subprocess import call
from clint.textui import puts, colored
from parajumper.db import create_date_binder, load_item, save_item, remove_item

EDITOR = os.environ.get('EDITOR', 'vim')
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
    if '-D' in args.flags:
        index = args.value_after('-D')
        return del_item(index, today, date_from, date_to, ago)
    if '-E' in args.flags:
        index = args.value_after('-E')
        return edit_item(index, today, date_from, date_to, ago)
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

def del_item(index, today=True, date_from=None, date_to=None, ago=None):
    """Delete one item from date binder."""
    if today:
        today = str(datetime.date.today())
        binder = create_date_binder(today)
    if (date_from is not None) or (date_to is not None):
        if ago is not None:
            binder = create_date_binder(date_from=date_from, offset=int(ago), date_to=date_to)
        else:
            binder = create_date_binder(date_from=date_from, offset=None, date_to=date_to)
    index = int(index)
    identity = binder.members[index]
    remove_item(identity)
    binder.members.remove(identity)
    show(level=0, today=today, date_from=date_from, date_to=date_to, ago=ago)

def edit_item(index, today=True, date_from=None, date_to=None, ago=None):
    """Edit item."""
    if today:
        today = str(datetime.date.today())
        binder = create_date_binder(today)
    if (date_from is not None) or (date_to is not None):
        if ago is not None:
            binder = create_date_binder(date_from=date_from, offset=int(ago), date_to=date_to)
        else:
            binder = create_date_binder(date_from=date_from, offset=None, date_to=date_to)
    index = int(index)
    identity = binder.members[index]

    initial_message = """<!-- Please enter your note below. You can use markdown -->
<!-- lines starting with '&' and a space are interpreted as tags -->
<!-- tags are separated by spaces, like this:-->
<!-- & history roman hannibal expected_in_test -->"""
    item = load_item(identity)
    notes = item.content
    tag_line = "& "
    for tag in item.tags:
        tag_line += tag
    tempf = tempfile.NamedTemporaryFile(suffix='.md', mode='w+', encoding='utf-8', delete=False)
    tempf.write(initial_message + '\n')
    tempf.write(notes + '\n')
    tempf.write(tag_line)
    tempf.flush()
    try:
        call([EDITOR, tempf.name])
    except FileNotFoundError:
        call(['vi', tempf.name])
    tempf.close()
    tags = []
    notes = ''
    with open(tempf.name) as tempf:
        for line in tempf:
            if line[:4] != '<!--':
                if line[:2] != '& ':
                    notes += line
                else:
                    tags = tags + [x for x in line[2:-1].split(' ') if x != '']
    os.remove(tempf.name)

    item.update(content=notes, tags=tags)
    save_item(item)
    show(level=0, today=today, date_from=date_from, date_to=date_to, ago=ago)
