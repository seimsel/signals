import platform
import os

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
