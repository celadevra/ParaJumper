"""ParaJumper main application entry point."""
from clint.arguments import Args
from clint.textui import puts, colored
import parajumper.cli.help as printhelp
import parajumper.cli.today as today
import parajumper.cli.new as new
import parajumper.cli.search as search
import parajumper.cli.tagged as tagged

COMMANDS_LIST = ['-h', '--help', 'help', 'day', 'tagged',
                 'search', 'new']
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
    if command == 5: # search
        search.dispatch(args)
    if command == 6: # new
        new.dispatch(args)

if __name__ == '__main__':
    main()
