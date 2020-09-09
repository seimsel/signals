from .external_application import ExternalApplication
from .utils.where import where

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

        env = {
            'UI_HTTP_URL': ui_http_url,
            'DEVELOPEMENT': 'true'
        }

        super().__init__(
            cmd,
            cwd='./signals-server',
            env=env
        )
