import os
import sys
import time
from tkinter import Tk, filedialog, simpledialog
import openpyxl as xl

sys.path.append(os.getcwd() + "/python")
from dowjones import config
from dowjones import Querier


def run(queryfile, begin_row, end_row=-1, begin_col=1):
    print("{} {}".format(queryfile, begin_row))
    wb = xl.load_workbook(queryfile)
    with Querier(begin_row) as q:
        q.start_random_mousemove(60)
        q.get_browser("chrome").open(config.dj_url)
        try:
            q.act_login(config.dj_username, config.dj_password)
            wb = q.query(wb, begin_row=begin_row, end_row=end_row, begin_col=begin_col, temp_file=queryfile + ".temp")
        except Exception as e:
            q.log(e)
            return q.query_row
        finally:
            wb.save(filename=queryfile)
        return 0


if __name__ == "__main__":
    os.environ['Path'] = os.environ['Path'] + os.path.pathsep + ".\\driver"

    tk = Tk()
    tk.withdraw()

    filename = sys.argv[1] if len(sys.argv) > 1 else filedialog.askopenfilename(title=u'选择查询文件',
                                                                                initialdir=(os.path.expanduser('.')))
    begin_row = sys.argv[2] if len(sys.argv) > 2 else simpledialog.askinteger(title=u'起始行数', prompt=u'请输入起始行数',
                                                                              initialvalue=1)

    end_row = sys.argv[3] if len(sys.argv) > 3 else simpledialog.askinteger(title=u'终止行数', prompt=u'请输入终止行数，-1表示最后一行',
                                                                            initialvalue=-1)
    begin_col = sys.argv[4] if len(sys.argv) > 4 else simpledialog.askinteger(title=u'起始列数', prompt=u'请输入起始列数',
                                                                              initialvalue=1)

    query_row = int(begin_row)
    end_row = int(end_row)
    begin_col = int(begin_col)
    while True:
        query_row = run(filename, query_row, end_row, begin_col)
        if query_row == 0:
            break

    time.sleep(10)
    tk.destroy()
