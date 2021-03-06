from time import sleep, strftime, localtime
from typing import Any, Callable
import threading
import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import pyautogui as pag
from across.pending import Pending


class Across:
    browser = None
    __random_mousemove_interval = 0

    def __init__(self):
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_track):
        self.__random_mousemove_interval = 0
        self.quit()

    ############################################################

    def get_browser(self, name):
        if name.lower() == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            self.browser = webdriver.Chrome(options=options)
        elif name.lower() == "firefox":
            profile = webdriver.FirefoxProfile()
            profile.accept_untrusted_certs = True
            self.browser = webdriver.Firefox(firefox_profile=profile)
        elif name.lower() == "ie":
            capabilities = webdriver.DesiredCapabilities().INTERNETEXPLORER
            capabilities['acceptSslCerts'] = True
            self.browser = webdriver.Ie(capabilities=capabilities)
        else:
            self.browser = None
        return self

    def open(self, url):
        self.browser.get(url)
        return self

    def pending(self, timeout: int = None, interval: int = 1):
        return Pending(timeout, interval)

    def quit(self):
        if self.browser is not None:
            self.browser.quit()

    def sleep(self, timeout):
        sleep(timeout)
        return self

    def wait(self, timeout, poll_frequency=0.5, ignored_exceptions=None):
        return WebDriverWait(self.browser, timeout, poll_frequency=poll_frequency,
                             ignored_exceptions=ignored_exceptions)

    ############################################################

    def chain(self):
        return ActionChains(self.browser)

    def expect(self, expect: Callable[[], Any], error_value: Any = False):
        try:
            return expect()
        except:
            return error_value

    def get_timestamp(self):
        return strftime("%Y-%m-%d %H:%M:%S", localtime())

    def input_text(self, el, text):
        el.clear()
        el.send_keys(text)
        return el

    def log(self, msg, end='\n', pure=False):
        if pure:
            print(msg, end=end, flush=True)
        else:
            print("[{}]{}".format(self.get_timestamp(), msg), end=end, flush=True)

    def record_table(self, table, xtract,
                     rows_selector=lambda table: table.find_elements_by_tag_name("tr"),
                     cells_selector=lambda row: row.find_elements_by_tag_name("td")):
        # result = []
        # for row in rows_selector(table):
        #     cells = cells_selector(row)
        #     result.append([cells[i].text for i in headers])
        # return result
        for t in xtract:
            if t[1] is None:
                t[1] = lambda cell: cell.text
        return [[t[1](cells[t[0]]) for t in xtract]
                for cells in [cells_selector(row) for row in rows_selector(table)]]

    def when(self, assertion: Callable[[], bool], error_value=False):
        def wrap():
            return self.expect(assertion, error_value)

        return wrap

    ############################################################

    def start_random_mousemove(self, interval):
        self.__random_mousemove_interval = interval

        def _random_mousemove():
            step = 1
            w, _ = pag.size()
            while self.__random_mousemove_interval > 0:
                try:
                    step *= -1
                    x, _ = pag.position()
                    if not ((x == 0 and step == -1) or (x == w - 1 and step == 1)):
                        pag.moveRel(step)
                except:
                    pass
                self.sleep(self.__random_mousemove_interval)

        threading.Thread(target=_random_mousemove, daemon=True).start()
        return self
