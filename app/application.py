from cefpython3 import cefpython as cef

from threading import Thread

import ctypes
import platform
import struct

class Application(Thread):
    def __init__(self, view):
        super().__init__()
        self.view = view

    def run(self):
        cef.Initialize()
        
        for window in self.view.windows:
            window_info = cef.WindowInfo()
            window_info.SetAsChild(
                window.winfo_id(),
                [0, 0, window.winfo_width(), window.winfo_height()]
            )
            browser = cef.CreateBrowserSync(
                window_info,
                url='http://localhost:8080'
            )

            def on_configure(event):
                width = event.width
                height = event.height
                system = platform.system()

                if system == 'Windows':
                    ctypes.windll.user32.SetWindowPos(
                        browser.GetWindowHandle(),
                        0, 0, 0, width, height, 0x0002
                    )

                elif system == 'Linux':
                    browser.SetBounds(0, 0, event.width, event.height)
                
                browser.NotifyMoveOrResizeStarted()

            window.bind('<Configure>', on_configure)

            def askopenfilenames(callback):
                def func():
                    filenames = window.askopenfilenames()
                    callback.Call(filenames)

                cef.PostTask(
                    thread=cef.TID_FILE,
                    func=func
                )
                

            bindings = cef.JavascriptBindings()
            bindings.SetFunction('askopenfilenames', askopenfilenames)
            browser.SetJavascriptBindings(bindings)

        cef.MessageLoop()
        cef.Shutdown()
