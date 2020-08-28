from cefpython3 import cefpython as cef
import sys

def main():
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize()
    cef.CreateBrowserSync(url="https://www.google.com/",
                          window_title="Hello World!")
    cef.MessageLoop()
    cef.Shutdown()

if __name__ == '__main__':
    main()