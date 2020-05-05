import os
import sys
import time
from tkinter import Tk, filedialog, simpledialog
import openpyxl as xl

sys.path.append(os.getcwd() + "/python")
from xingshi import Querier


def run(queryfile, begin_row, end_row=-1):
    print("{} {}".format(queryfile, begin_row))
    wb = xl.load_workbook(queryfile)
    with Querier(begin_row) as q:
        q.start_random_mousemove(60)
        q.get_browser("chrome").open("https://www.chineseinla.com/lastname.html")
        q.sleep(3)
        try:
            wb = q.query(wb, begin_row=begin_row, end_row=end_row, temp_file=queryfile + ".temp")
        except Exception as e:
            q.log(e)
            return q.query_row
        finally:
            wb.save(filename=queryfile)
        return 0


if __name__ == "__main__":
    os.environ['Path'] = os.environ['Path'] + os.path.pathsep + ".\\driver"

    run("e:/python/across/data/xingshi.xlsx", 1)
