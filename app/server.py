from .external_application import ExternalApplication
from .utils.where import where

import os

class Server(ExternalApplication):
    def __init__(
        self,
        ui_http_url='http://localhost:8080',
        server_port=8000,
        development=False
    ):
        cmd = [
            where('uvicorn'), 'signals.server:app',
            '--port', f'{server_port}'
        ]

        if development:
            cmd.extend([
                '--reload'
            ])

        super().__init__(
            cmd,
            cwd='./signals-server',
            env={
                'UI_HTTP_URL': ui_http_url,
                'SYSTEMROOT': os.environ['SYSTEMROOT'],
                'SYSTEMDRIVE': os.environ.get('SYSTEMDRIVE'),
                'HOME': os.environ.get('USERPROFILE', os.environ.get('HOME')),
                'DEVELOPEMENT': 'true'
            }
        )
