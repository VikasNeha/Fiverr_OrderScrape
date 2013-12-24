outputPath = None
outputAttachmentsPath = None
baseURL = 'http://fiverr.com/login'
webElementTimeOut = 10
Orders = []
ScrapedOrders = []
FivUsername = None
FivPassword = None


import sys
import os
import imp


def main_is_frozen():
    return (hasattr(sys, "frozen") or  # new py2exe
            hasattr(sys, "importers")  # old py2exe
            or imp.is_frozen("__main__"))  # tools/freeze


def get_main_dir():
    if main_is_frozen():
        return os.path.dirname(os.path.dirname(sys.executable))
    return os.path.dirname(sys.argv[0])