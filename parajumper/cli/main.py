"""ParaJumper main application entry point."""
from clint.arguments import Args
from clint.textui import puts, colored
import parajumper.cli.help as printhelp

def main():
    """PJ's main entry function"""
    commands_list = ['help', 'today',
                     'reschedule', 'pin',
                     'tag', 'export',
                     'new', 'move', 'edit', 'del', 'delete']
    args = Args()
    if len(args) == 0:
        args = Args(['today'])
    try:
        command = commands_list.index(args[0])
    except ValueError:
        command = 0
        puts(colored.red("Unknown command: %s" % args[0]))
    if command == 0: # help
        if (not args.has(1)) or (args.not_flags[1] not in commands_list):
            printhelp.default_help()
            
if __name__ == '__main__':
    main()
