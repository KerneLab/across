import os
import sys
import time
import re
from datetime import datetime, timedelta
from tkinter import Tk, filedialog, simpledialog
import openpyxl as xl

sys.path.append(os.getcwd() + "/python")
from biding import Querier


def run():
    with Querier() as q:
        q.get_browser("chrome").open("http://www.bidchance.com/freesearch.do?searchtype=zb&queryword=xray")
        q.query("反洗钱")


if __name__ == "__main__":
    os.environ['Path'] = os.environ['Path'] + os.path.pathsep + ".\\driver"

    run()
