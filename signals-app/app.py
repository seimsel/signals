from signals.devserver import DevServer
from signals.server import Server
from signals.view import View
from signals.application import Application

from argparse import ArgumentParser
from contextlib import nullcontext

from signals.config import get_config

def main(args):
    development = args.development
    config = get_config(development)
    server = Server(
        config['ui_http_url'],
        config['server_port'],
        config['development']
    )
    devserver = DevServer(
        config['ui_http_url'],
        config['server_http_url'],
        config['server_ws_url']
    ) if development else nullcontext()

    with server:
        with devserver:
            application = Application()
            view = View(config['ui_http_url'])
            application.start()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--development', action='store_true')
    args = parser.parse_args()
    main(args)
