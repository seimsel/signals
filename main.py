from cefpython3 import cefpython as cef
from dotenv import load_dotenv
from psutil import Process

from contextlib import contextmanager
from subprocess import Popen
import sys
import os
import signal
import platform

def where(file_name):
    # inspired by http://nedbatchelder.com/code/utilities/wh.py
    # see also: http://stackoverflow.com/questions/11210104/
    path_sep = ":" if platform.system() == "Linux" else ";"
    path_ext = [''] if platform.system() == "Linux" or '.' in file_name else os.environ["PATHEXT"].split(path_sep)
    for d in os.environ["PATH"].split(path_sep):
        for e in path_ext:
            file_path = os.path.join(d, file_name + e)
            if os.path.exists(file_path):
                return file_path
    raise Exception(file_name + " not found")

@contextmanager
def process(*args, **kwargs):
    # https://gist.github.com/jizhilong/6687481#gistcomment-3057122
    proc = Popen(*args, **kwargs)
    try:
        yield proc
    finally:
        for child in Process(proc.pid).children(recursive=True):
            child.terminate()
        proc.terminate()

def main():
    with process(
        [ where('npm'), 'run', 'dev' ],
        cwd='./signals-ui',
        env={
            'NODE_ENV': 'development',
            'UI_HTTP_URL': 'http://localhost:8080',
            'SERVER_HTTP_URL': 'http://localhost:8000',
            'SERVER_WS_URL': 'ws://localhost:8000',
            'SYSTEMROOT': os.environ['SYSTEMROOT'],
            'APPDATA': os.environ['APPDATA'],
            'PATH': os.environ['PATH']
        }
    ):

        with process(
            [
                where('uvicorn'), 'signals.server:app',
                '--reload'
            ],
            cwd='./signals-server',
            env={
                'UI_HTTP_URL': 'http://localhost:8080',
                'SYSTEMROOT': os.environ['SYSTEMROOT'],
                'SYSTEMDRIVE': os.environ.get('SYSTEMDRIVE'),
                'HOME': os.environ.get('USERPROFILE', os.environ.get('HOME'))
            }
        ):

            sys.excepthook = cef.ExceptHook
            cef.Initialize()
            cef.CreateBrowserSync(url='http://localhost:8080')
            cef.MessageLoop()
            cef.Shutdown()

if __name__ == '__main__':
    main()
