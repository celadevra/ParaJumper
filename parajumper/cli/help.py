"""Show help to various commands and arguments of ParaJumper."""

from clint.textui import puts, indent, colored

def default_help():
    """Default help message, invoked with 'pj help' or 'pj --help'."""
    puts("Usage: pj [command [<binder selector>] [<item selector>]]")
    puts("       pj -h/--help/help: show help")
    puts("")
    puts("Supported commands:")
    with indent(4):
        puts(colored.yellow("new"))
    with indent(6):
        puts("Create new items and binders.")
    with indent(4):
        puts(colored.yellow("today"))
    with indent(6):
        puts("Default command. Show today's binder.")
