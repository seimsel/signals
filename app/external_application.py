from subprocess import Popen
from psutil import Process

class ExternalApplication:
    def __init__(self, cmd, cwd=None, env=None):
        self.process = None
        self.cmd = cmd
        self.cwd = cwd
        self.env = env

    def __enter__(self):
        self.process = Popen(
            self.cmd,
            cwd=self.cwd,
            env=self.env
        )
        return self.process

    def __exit__(self, *args, **kwargs):
        for child in Process(self.process.pid).children(recursive=True):
            child.terminate()
        self.process.terminate()
