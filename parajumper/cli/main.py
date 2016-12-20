"""ParaJumper main application entry point."""
from clint.arguments import Args
from clint.textui import puts, colored
import parajumper.cli.help as printhelp
import parajumper.cli.today as today
import parajumper.cli.new as new
import parajumper.cli.tag as tag
import parajumper.cli.tagged as tagged

COMMANDS_LIST = ['-h', '--help', 'help', 'day', 'tagged',
                 'reschedule', 'pin',
                 'tag', 'export',
                 'new', 'move', 'edit', 'del', 'delete']
def main():
    """PJ's main entry function"""
    args = Args()
    if len(args) == 0:
        args = Args(['day'])
    try:
        command = COMMANDS_LIST.index(args[0])
    except ValueError:
        command = 0
        puts(colored.red("Unknown command: %s" % args[0]))
    if command <= 2: # help
        printhelp.dispatch(args, COMMANDS_LIST)
    if command == 3: # day
        today.dispatch(args)
    if command == 4: # tagged
        tagged.dispatch(args)
    if command == 9: # new
        new.dispatch(args)
    if command == 7: # tag
        tag.dispatch(args)

if __name__ == '__main__':
    main()
