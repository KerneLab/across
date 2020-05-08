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
    wb = xl.Workbook()
    fn = "data/biding.xlsx"
    with Querier() as q:
        q.get_browser("chrome").open("http://www.bidchance.com/freesearch.do?searchtype=zb&queryword=xray")
        try:
            q.query(wb, fn, "反洗钱")
        except Exception as e:
            q.log(e)
        finally:
            wb.save(filename=fn)


if __name__ == "__main__":
    os.environ['Path'] = os.environ['Path'] + os.path.pathsep + ".\\driver"

    run()
