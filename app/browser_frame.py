from cefpython3 import cefpython as cef

from tkinter import Frame
from tkinter.filedialog import askopenfilenames

class BrowserFrame(Frame):
    def __init__(self, master):
        super().__init__(
            master,
            width=800,
            height=600,
            bg='#1e1e1e'
        )
        self.pack(fill='both', expand=True)

    def askopenfilenames(self):
        return askopenfilenames(parent=self)
