"""Handles search command."""
from clint.textui import puts, colored
from parajumper.db import create_search_binder, load_item

def dispatch(args):
    """Dispatcher for search command."""
    args.remove('search')
    notflag = args.not_flags.all
    verbosity = args.value_after('-v')
    return get_binder(verbosity, *notflag)

def get_binder(level=0, *terms):
    """Get binder by search terms."""
    binder = create_search_binder(*terms)
    print(binder)
    items = []
    index = 0
    for member in binder.members:
        items.append(load_item(member))
    for item in items:
        puts(colored.blue("[%2d]" % index))
        print(item.__str__(verbose=level))
        index += 1
