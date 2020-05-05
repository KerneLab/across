import re
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from across import Across
from zhtools.langconv import chs_to_cht


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

    def act_wait_ready(self):
        return self.wait(5).until(ec.presence_of_element_located((By.CSS_SELECTOR, "form.search")))

    def act_query(self, text):
        form = self.act_wait_ready()
        input = form.find_element_by_id("SN")
        button = form.find_element_by_css_selector("input[type='submit']")
        self.input_text(input, text)
        button.click()

    def act_wait_result(self, text):
        def checked():
            table = self.browser.find_element_by_css_selector("table.result")
            return table.find_element_by_css_selector("td.alm-c").text == text

        self.sleep(0.5 + random.random() * 0.5)
        self.pending(10).until(self.when(checked))

    def act_record_query_result(self):
        table = self.wait(5).until(ec.presence_of_element_located((By.CSS_SELECTOR, "table.result")))
        rows = table.find_elements_by_tag_name("tr")
        if len(rows) <= 2:
            return None
        else:
            def xtract_cell(cell):
                # <span>zhai</span><span>di</span>
                text = re.sub(r"<span>([^<]+)</span>", r"\1 ", cell.get_attribute('innerHTML')).strip()
                return " ".join(set(re.split(r"\s+", text)))

            xtract = [[0, xtract_cell]]
            results = self.record_table(table, xtract,
                                        rows_selector=lambda table: table.find_elements_by_tag_name("tr")[1:-1])
            return [v[0] for i, v in enumerate(results)]

    def query(self, workbook, begin_row=1, end_row=-1, temp_file=None):
        sheet = workbook.get_sheet_by_name(workbook.get_sheet_names()[0])
        offset = 2
        for i, row in enumerate(sheet.rows):
            r = i + 1
            if 0 < end_row < r:
                break
            if r < begin_row:
                continue
            self.query_row = r
            text = chs_to_cht(row[0].value)
            if text.strip() == "":
                continue
            self.log("Row:{} Query:{} ... ".format(r, text), end='')
            self.act_query(text)
            self.act_wait_result(text)
            result = self.act_record_query_result()
            if result is None:
                sheet.cell(r, offset, "")
            else:
                [sheet.cell(r, offset + j, v) for j, v in enumerate(result)]
            if temp_file is not None:
                workbook.save(filename=temp_file)
            self.log("Done", pure=True)
        return workbook
