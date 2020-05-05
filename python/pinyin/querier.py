import re
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from across import Across


class Querier(Across):
    @property
    def query_row(self):
        return self.__query_row

    @query_row.setter
    def query_row(self, value):
        self.__query_row = value

    def __init__(self, begin_row):
        super(Querier, self).__init__()
        self.query_row = begin_row

    def act_query(self, text):
        form = self.browser.find_element_by_id("lastnameForm")
        input = form.find_element_by_id("lastname")
        button = form.find_element_by_name("Search")
        self.input_text(input, text)
        button.click()

    def act_record_query_result(self):
        result_panel = self.browser.find_element_by_id("name_list_block")
        result_table = self.expect(lambda: result_panel.find_element_by_css_selector("table.name_list"), None)
        if result_table is None:
            return None
        else:
            xtract = [[0, None],
                      [1, None],
                      [2, None],
                      [3, None],
                      [4, None],
                      [5, None],
                      [6, None],
                      [7, None]]
            return self.record_table(result_table, xtract,
                                     rows_selector=lambda table: table.find_elements_by_tag_name("tr")[1:])

    def query(self, workbook, begin_row=1, end_row=-1, temp_file=None):
        sheet = workbook.get_sheet_by_name(workbook.get_sheet_names()[0])
        offset = 1
        for i, row in enumerate(sheet.rows):
            r = i + 1
            if 0 < end_row < r:
                break
            if r < begin_row:
                continue
            self.query_row = r
            text = row[0].value
            if text.strip() == "":
                continue
            self.log("Row:{} Query:{} ... ".format(r, text), end='')
            self.act_query(text)
            self.sleep(1 + random.random())
            result = self.act_record_query_result()
            if result is None:
                sheet.cell(r, offset + 1, "")
            else:
                [sheet.cell(r, offset + j, v) for j, v in enumerate(result)]
            if temp_file is not None:
                workbook.save(filename=temp_file)
            self.log("Done", pure=True)
        return workbook
