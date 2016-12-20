"""Handle search with tags."""
import parajumper.db as db

def dispatch(args):
    """Dispatcher for tagged command."""
    args.remove('tagged') 
    tags = args.not_flags.all
    verbosity = args.value_after('-v')
    tagged_binder(verbosity, *tags)

def tagged_binder(verbosity=0, *tags):
    """Generate and show binder populated with items with any of the tags."""
    binder = db.create_tag_binder(tags)
    print(binder)
    items = []
    index = 0
    for member in binder.members:
        items.append(load_item(member))
    for item in items:
        puts(colored.blue("[%2d]" % index))
        print(item.__str__(verbose=level))
        index += 1


