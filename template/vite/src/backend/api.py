import webview as wv
import sys
import os
from pyder import *

class API:
    def __init__(self):
        self.window = wv.active_window()
        self.appID = f"{pyder_domainSystem}.{pyder_projectID}"

    def getConfigPath(self):
        if sys.platform == "win32":
            base = os.environ.get("APPDATA", "")
        elif sys.platform == "darwin":
            base = os.path.join(os.path.expanduser("~"), "Library", "Application Support")
        else:
            base = os.path.join(os.path.expanduser("~"), ".config")
        return os.path.join(base, self.appID)