from signals.devserver import DevServer
from signals.server import Server
from signals.view import View
from signals.application import Application
from signals.config import get_config

import sys

from argparse import ArgumentParser
from contextlib import nullcontext

def main(args):
    development = args.development
    bundle = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

    config = get_config(bundle=bundle)
    server = Server(
        config['ui_http_url'],
        config['server_port'],
        development,
        bundle
    )
    devserver = DevServer(
        config['ui_http_url'],
        config['server_http_url'],
        config['server_ws_url'],
        development
    ) if not bundle else nullcontext()

    with server:
        with devserver:
            application = Application()
            view = View(
                config['ui_http_url'],
                development
            )
            application.start()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--development', action='store_true')
    args = parser.parse_args()
    main(args)
