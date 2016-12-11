"""ParaJumper main application entry point."""
from cement.core.exc import CaughtSignal
from cement.core.foundation import CementApp

class PJApp(CementApp):
    """Cement app class for PJ"""
    class Meta:
        """Metadata for PJApp class"""
        label = 'pj'

APP = PJApp()

def main():
    """PJ's main entry function"""
    try:
        code = 0
        APP.run()
    except CaughtSignal as error:
        code = 0
        print(error)
    except Exception as error:
        code = 1
        print(error)

    APP.close(code)

if __name__ == '__main__':
    main()
