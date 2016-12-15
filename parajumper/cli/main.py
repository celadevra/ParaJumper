"""ParaJumper main application entry point."""
from clint.arguments import Args
from clint.textui import puts, colored
import parajumper.cli.help as printhelp
import parajumper.cli.today as today
import parajumper.cli.new as new

COMMANDS_LIST = ['-h', '--help', 'help', 'today',
                 'reschedule', 'pin',
                 'tag', 'export',
                 'new', 'move', 'edit', 'del', 'delete']
def main():
    """PJ's main entry function"""
    args = Args()
    if len(args) == 0:
        args = Args(['today'])
    try:
        command = COMMANDS_LIST.index(args[0])
    except ValueError:
        command = 0
        puts(colored.red("Unknown command: %s" % args[0]))
    if command <= 2: # help
        printhelp.dispatch(args, COMMANDS_LIST)
    if command == 3: # today
        today.dispatch(args)
    if command == 8: # new
        new.dispatch(args)

if __name__ == '__main__':
    main()
