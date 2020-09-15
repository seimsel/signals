def get_config(development=False):
    server_port = 8000

    config = {
        'development': 'true' if development else 'false',
        'ui_http_url': 'http://localhost:8080' if development else 'http://localhost:8000',
        'server_port': f'{server_port}',
        'server_http_url': f'http://localhost:{server_port}',
        'server_ws_url': f'ws://localhost:{server_port}'
    }
    
    return config
