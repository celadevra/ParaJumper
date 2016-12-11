"""ParaJumper main application entry point."""
from cement.core.exc import CaughtSignal
from cement.core.foundation import CementApp
from cement.ext.ext_argparse import ArgParseArgumentHandler

class PJArgHandler(ArgParseArgumentHandler):
    class Meta:
        label = 'pj_args_handler'

        def error(self, message):
            """Error handling for arg parsing"""
            super(PJArgHandler, self).error("unknown args")

class PJApp(CementApp):
    """Cement app class for PJ"""
    class Meta:
        """Metadata for PJApp class"""
        label = 'pj'
        arg_handler = PJArgHandler

APP = PJApp()

def main():
    """PJ's main entry function"""
    try:
        APP.setup()
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
