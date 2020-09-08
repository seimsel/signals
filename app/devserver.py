from .external_application import ExternalApplication
from .utils.where import where

import os

class DevServer(ExternalApplication):
    def __init__(
        self,
        ui_http_url='http://localhost:8080',
        server_http_url='http://localhost:8000',
        server_ws_url='ws://localhost:8000'
    ):
        super().__init__(
            cmd=[ where('npm'), 'run', 'dev' ],
            cwd='./signals-ui',
            env={
                'NODE_ENV': 'development',
                'UI_HTTP_URL': ui_http_url,
                'SERVER_HTTP_URL': server_http_url,
                'SERVER_WS_URL': server_ws_url,
                'SYSTEMROOT': os.environ['SYSTEMROOT'],
                'APPDATA': os.environ['APPDATA'],
                'PATH': os.environ['PATH']
            }
        )
