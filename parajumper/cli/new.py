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

def newitem():
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
    tags = []
    with tempfile.NamedTemporaryFile(suffix='.md') as tempf:
        tempf.write(str.encode(initial_message))
        tempf.flush()
        try:
            call([EDITOR, tempf.name])
        except FileNotFoundError:
            call(['vi', tempf.name])

        tempf.seek(0)
        for line in tempf:
            if bytes.decode(line[:4]) != '<!--':
                if bytes.decode(line[:2]) != '& ':
                    notes += bytes.decode(line)
                else:
                    tags = tags + [x for x in bytes.decode(line[2:-1]).split(' ') if x != '']
    result = item.Item(bullet=bullet, content=re.sub('\n+$', '\n', notes), tags=tags)
    db.save_item(result)
    puts("New item saved with id = %s" % colored.green(result.identity))
