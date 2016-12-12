"""Show help to various commands and arguments of ParaJumper."""

from clint.textui import puts, indent

def default_help():
    """Default help message, invoked with 'pj help' or 'pj --help'."""
    puts("Usage: pj [command [<binder selector>] [<item selector>]]")
