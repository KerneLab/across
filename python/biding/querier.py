import re
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from across import Across


class Querier(Across):
    def __init__(self):
        super(Querier, self).__init__()

    def act_query(self, text):
        input = self.wait(5).until(ec.presence_of_element_located((By.ID, "queryword")))
        button = self.wait(5).until(ec.presence_of_element_located((By.ID, "submitsearch")))
        self.input_text(input, text)
        button.click()

    def act_wait_result(self):
        next = self.wait(10).until(ec.presence_of_element_located((By.ID, "nextpage2")))
        table = self.wait(10).until(ec.presence_of_element_located((By.ID, "togglefont")))
        return next, table

    def act_record_result(self, table):
        def xtract_link_name(cell):
            return cell.find_element_by_tag_name("a").text

        def xtract_url(cell):
            return cell.find_element_by_tag_name("a").get_attribute("href")

        xtract = [[0, None],
                  [1, xtract_link_name],
                  [1, xtract_url],
                  [2, None],
                  [3, None]]
        return self.record_table(table, xtract,
                                 rows_selector=lambda t: t.find_elements_by_css_selector("tr.datatr"))

    def query(self, text):
        self.act_query(text)
        count = 0
        while count < 5:
            count += 1
            self.sleep(0.5 + random.random() * 0.5)
            next, table = self.act_wait_result()
            result = self.act_record_result(table)
            print(result)
            if "okgo" in set(re.split(r"\s+", next.get_attribute("class"))):
                next.find_element_by_css_selector("a.nextpagea").click()
            else:
                break
