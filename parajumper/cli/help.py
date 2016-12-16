"""Show help to various commands and arguments of ParaJumper."""

import sys
from clint.textui import puts, indent, colored

def dispatch(args, commands):
    """Dispatch various help functions."""
    if (not args.not_flags.has(1)) or (args.not_flags[1] not in commands):
        default_help()
    elif args.not_flags.has(1):
        if args.not_flags[1] in commands:
            # use sys to get current module name, and determine which help func to call
            # with getattr()
            method_to_call = getattr(sys.modules[__name__], args.not_flags[1] + '_help')
            method_to_call()
        else:
            default_help()

def default_help():
    """Default help message, invoked with 'pj help' or 'pj --help'."""
    puts("Usage: pj [command [<binder selector>] [<item selector>]]")
    puts("       pj -h/--help/help: show help")
    puts("       pj help <command>: show help for <command>")
    puts("")
    puts("Supported commands:")
    with indent(4):
        puts(colored.yellow("new"))
    with indent(6):
        puts("Create new items and binders.")
    with indent(4):
        puts(colored.yellow("day"))
    with indent(6):
        puts("Default command. Show today's binder by default.")

def day_help():
    """Help messages for day command."""
    puts("Usage: pj day [-v/-vv/-vvv] [-df] [-dt] [-da]")
    puts("")
    puts("Show the day's items. -v/-vv/-vvv for showing more attributes of the item.")
    puts("-df <YYYY-MM-DD> to specify starting date.")
    puts("-dt <YYYY-MM-DD> to specify ending date.")
    puts("-da <N> to specify how many days ago or in the future.")

def new_help():
    """Help messages for new command."""
    puts("Usage: pj new [-T <tag1,tag2,...>] [-t/-e/-n <content>]")
    puts("")
    puts("Create new entry. By default schedule to current day.")
    puts("Interactive editing needs your $EDITOR or vi to be available.")
    puts("pj new -T specifies tags for item being created.")
    puts("pj new -t/-e/-n creates notes from following quoted text.")
    puts("-T and -t/-e/-n can be used together.")
