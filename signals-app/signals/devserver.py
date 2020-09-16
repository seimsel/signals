from .external_application import ExternalApplication
from .utils.where import where
from pathlib import Path

class DevServer(ExternalApplication):
    def __init__(
        self,
        ui_http_url,
        server_http_url,
        server_ws_url
    ):
        super().__init__(
            cmd=[ where('npm'), 'run', 'dev' ],
            cwd='../signals-ui',
            env={
                'NODE_ENV': 'development',
                'UI_HTTP_URL': ui_http_url,
                'SERVER_HTTP_URL': server_http_url,
                'SERVER_WS_URL': server_ws_url
            }
        )
