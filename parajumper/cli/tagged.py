"""Handle search with tags."""
import parajumper.db as db

def dispatch(args):
    """Dispatcher for tagged command."""
    args.remove('tagged') 
    tags = args.not_flags.all
    db.create_tag_binder(tags)

