from .external_application import ExternalApplication
from .utils.where import where
from pathlib import Path

class Server(ExternalApplication):
    def __init__(
        self,
        ui_http_url,
        server_port,
        development
    ):

        if development:
            cmd = [
                where('python'), str(Path(__file__).parent.parent.with_name('signals-server')/'server.py')
            ]
        else:
            cmd = [
                './SignalsServer'
            ]

        env = {
            'UI_HTTP_URL': ui_http_url,
            'SERVER_PORT': server_port,
            'DEVELOPMENT': development
        }

        super().__init__(
            cmd,
            env=env
        )
