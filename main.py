from app.devserver import DevServer
from app.server import Server
from app.view import View
from app.application import Application

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView

import sys

from argparse import ArgumentParser
from contextlib import nullcontext
from time import sleep

def main(args):
    development = args.development
    server = Server(development=development)
    devserver = DevServer() if development else nullcontext()

    with server:
        with devserver:
            application = Application()
            view = View()
            application.start()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--development', action='store_true')
    args = parser.parse_args()
    main(args)
