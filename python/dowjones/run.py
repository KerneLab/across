import os
import sys
import time
from tkinter import Tk, filedialog, simpledialog
import openpyxl as xl

sys.path.append(os.getcwd() + "/python")
from dowjones import config
from dowjones import Querier


def run(queryfile, begin_row, tempfile='data/temp.xlsx'):
    print("{} {}".format(queryfile, begin_row))
    wb = xl.load_workbook(queryfile)
    with Querier() as q:
        q.start_random_mousemove(60)
        q.get_browser("chrome").open(config.dj_url)
        q.act_login(config.dj_username, config.dj_password)
        try:
            wb = q.query(wb, begin_row=begin_row, temp_file=tempfile)
        except Exception as e:
            q.log(e)
        wb.save(filename=queryfile)


if __name__ == "__main__":
    os.environ['Path'] = os.environ['Path'] + os.path.pathsep + ".\\driver"

    tk = Tk()
    tk.withdraw()

    filename = sys.argv[1] if len(sys.argv) > 1 else filedialog.askopenfilename(title=u'选择查询文件',
                                                                                initialdir=(os.path.expanduser('.')))
    begin_row = sys.argv[2] if len(sys.argv) > 2 else simpledialog.askinteger(title=u'起始行数', prompt=u'请输入起始行数',
                                                                              initialvalue=1)

    run(filename, int(begin_row))

    time.sleep(10)
    tk.destroy()
