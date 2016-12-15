"""module to handle 'new' command."""

import tempfile
import os
import re
from subprocess import call
from clint.textui import prompt, puts, indent, colored
import parajumper.item as item
import parajumper.config as config
import parajumper.db as db

EDITOR = os.environ.get('EDITOR', 'vim')

def dispatch(args):
    """Dispatcher for new command."""
    if '-T' in args:
        tags = args.value_after('-T').split(',')
    if not args.flags.has(0):
        newitem()
    elif '-t' in args:
        newtodo(args.value_after('-t'), tags)
    elif '-e' in args:
        newevent(args.value_after('-e'), tags)
    elif '-n' in args:
        newnote(args.value_after('-n'), tags)

def newitem(tags=None):
    """Create new item by calling default $EDITOR, read in user input, and parse content."""
    conf = config.Config()
    bullets = conf.options['bullets']
    puts("Please select a bullet for your note.")
    puts("Available bullets are:")
    for key in bullets:
        with indent(4):
            puts("%s : %s" % (key, bullets[key]))
    bullet = prompt.query("Your choice: ")
    initial_message = """<!-- Please enter your note below. You can use markdown -->
<!-- lines starting with '&' and a space are interpreted as tags -->
<!-- tags are separated by spaces, like this:-->
<!-- & history roman hannibal expected_in_test -->"""
    notes = ''
    if tags is None:
        tags = []
    with tempfile.NamedTemporaryFile(suffix='.md', mode='w+', encoding='utf-8') as tempf:
        tempf.write(initial_message)
        tempf.flush()
        try:
            call([EDITOR, tempf.name])
        except FileNotFoundError:
            call(['vi', tempf.name])

        tempf.seek(0)
        for line in tempf:
            if line[:4] != '<!--':
                if line[:2] != '& ':
                    notes += line
                else:
                    tags = tags + [x for x in line[2:-1].split(' ') if x != '']
    result = item.Item(bullet=bullet, content=re.sub('\n+$', '\n', notes), tags=tags)
    db.save_item(result)
    puts("New item saved with id = %s" % colored.green(result.identity))

def _find_bullet(what):
    """Find bullet char corresponding to string."""
    conf = config.Config()
    bullets = conf.options['bullets']
    return list(bullets.keys())[list(bullets.values()).index(what)]

def newtodo(note, tags=None):
    """Quickly (non-interactively) create and store a new todo item."""
    result = item.Item(bullet=_find_bullet('todo'), content=note, tags=tags)
    db.save_item(result)
    puts("New item saved with id = %s" % colored.green(result.identity))

def newevent(note, tags=None):
    """Quickly (non-interactively) create and store a new event item."""
    result = item.Item(bullet=_find_bullet('event'), content=note, tags=tags)
    db.save_item(result)
    puts("New item saved with id = %s" % colored.green(result.identity))

def newnote(note, tags=None):
    """Quickly (non-interactively) create and store a new note item."""
    result = item.Item(bullet=_find_bullet('notes'), content=note, tags=tags)
    db.save_item(result)
    puts("New item saved with id = %s" % colored.green(result.identity))
