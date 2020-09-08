from .browser_frame import BrowserFrame

from threading import Thread
from tkinter import Tk

class View(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        self.root = Tk()
        
        self.windows = [
            BrowserFrame(self.root)
        ]
        self.root.mainloop()
