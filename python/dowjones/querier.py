import re
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

    def act_login(self, username, password):
        # 获取登录面板
        panel = self.wait(180).until(ec.presence_of_element_located((By.ID, "card-sign-in")))
        self.pending(180).until(self.when(lambda: len(panel.find_elements_by_tag_name("button")) > 0))
        # 输入用户名
        self.input_text(panel.find_element_by_id("email"), username)
        # 输入密码
        self.input_text(panel.find_element_by_id("password"), password)
        self.pending(180, 5).until(self.when(lambda: panel.find_elements_by_tag_name("button")[0].click() is None))

    def act_wait_query_page(self):
        # 等待查询界面完整加载
        self.wait(180).until(ec.presence_of_element_located((By.ID, "divDownButtons")))

    def act_query(self, text):
        # 搜索按钮面板
        query_panel = self.browser.find_element_by_id("divnonubo")
        query_button = query_panel.find_element_by_css_selector("input[value='搜索']")
        # 查询输入面板
        input_panel = self.browser.find_element_by_id("divAdvanceSearch")
        search_input = input_panel.find_element_by_id("txtName")
        # 执行查询
        self.input_text(search_input, text)
        query_button.click()

    def act_wait_query_result(self):
        result_panel = self.wait(30).until(ec.presence_of_element_located((By.ID, "ResultsDiv1")))
        self.pending(180).until(
            lambda: self.expect(lambda: result_panel.find_element_by_id("table_1") is not None)
                    or self.expect(lambda: result_panel.find_element_by_id("lblNoResults1").text.strip() != ""))

    def act_record_query_result(self):
        result_panel = self.browser.find_element_by_id("ResultsDiv1")
        if result_panel.find_element_by_id("lblNoResults1").text.strip() != "":
            # 没有相关纪录
            return None
        else:
            result_table = result_panel.find_element_by_id("table_1")

            def xtract_img_title(cell):
                return cell.find_elements_by_tag_name("img")[0].get_attribute("title")

            def xtract_name_id(cell):
                # javascript:ShowHoverText(event,"40405","Hajj Osama Bin Laden","男性","1-1-1957","精确","","10")
                return re.sub(r'.+?\(event,"([^"]+?)".*', r"\1",
                              cell.find_elements_by_tag_name("a")[0].get_attribute("onmouseover"))

            def xtract_name_matched(cell):
                # javascript:ShowHoverText(event,"40405","Hajj Osama Bin Laden","男性","1-1-1957","精确","","10")
                return re.sub(r'.+?\(event,"(?:[^"]+?)","(.+?)",".*', r"\1",
                              cell.find_elements_by_tag_name("a")[0].get_attribute("onmouseover"))

            xtract = [[0, xtract_img_title],
                      [4, xtract_name_id],
                      [4, xtract_name_matched],
                      [4, None],
                      [5, None],
                      [6, None],
                      [7, None],
                      [8, None]]
            return self.record_table(result_table, xtract,
                                     rows_selector=lambda table: table.find_elements_by_tag_name("tr")[0:1])[0]

    def act_return_query(self):
        return_panel = self.browser.find_element_by_id("divTopSearchResults")
        return_panel.find_element_by_css_selector("input[value^='重新搜索']").click()

    def query(self, workbook, begin_row=1, end_row=-1, begin_col=1, temp_file=None):
        sheet = workbook.get_sheet_by_name(workbook.get_sheet_names()[0])
        offset = begin_col
        for i, row in enumerate(sheet.rows):
            r = i + 1
            if 0 < end_row < r:
                break
            if r < begin_row:
                continue
            self.query_row = r
            name = row[offset - 1].value
            if name.strip() == "":
                continue
            self.log("Row:{} Query:{} ... ".format(r, name), end='')
            self.act_wait_query_page()
            self.act_query(name)
            self.act_wait_query_result()
            result = self.act_record_query_result()
            if result is None:
                sheet.cell(r, offset + 1, "没有相关纪录")
            else:
                [sheet.cell(r, offset + 1 + j, v) for j, v in enumerate(result)]
            if temp_file is not None:
                workbook.save(filename=temp_file)
            self.log("Done", pure=True)
            self.act_return_query()
        return workbook
