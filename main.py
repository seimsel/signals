from app.devserver import DevServer
from app.server import Server
from app.view import View
from app.application import Application

from cefpython3 import cefpython as cef

import sys

from argparse import ArgumentParser
from contextlib import nullcontext
from time import sleep

def main(args):
    sys.excepthook = cef.ExceptHook
    development = args.development
    server = Server(development=development)
    devserver = DevServer() if development else nullcontext()

    with server:
        with devserver:
            view = View()
            view.start()

            application = Application(view)
            application.start()

            while application.is_alive() and view.is_alive():
                try:
                    sleep(0.5)
                except KeyboardInterrupt:
                    view.root.quit()
                    view.root.update()
                    break

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--development', action='store_true')
    args = parser.parse_args()
    main(args)
