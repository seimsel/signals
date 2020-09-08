from cefpython3 import cefpython as cef

from tkinter import Frame

class BrowserFrame(Frame):
    def __init__(self, root):
        super().__init__(
            root,
            width=800,
            height=600,
            bg='#1e1e1e'
        )
        self.pack(fill='both', expand=True)
