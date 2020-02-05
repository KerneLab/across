from time import sleep, strftime, localtime
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait


class Across:
    browser = None

    def __init__(self):
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_track):
        self.quit()

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

    def pending(self, interval, assertion):
        while True:
            if self.decide(assertion):
                return self
            else:
                sleep(interval)

    def quit(self):
        if self.browser is not None:
            self.browser.quit()

    def sleep(self, timeout):
        sleep(timeout)
        return self

    def wait(self, timeout, poll_frequency=0.5, ignored_exceptions=None):
        return WebDriverWait(self.browser, timeout, poll_frequency=poll_frequency,
                             ignored_exceptions=ignored_exceptions)

    ###############################################################

    def chain(self):
        return ActionChains(self.browser)

    def decide(self, assertion):
        try:
            return assertion()
        except:
            return False

    def get_timestamp(self):
        return strftime("%Y-%m-%d %H:%M:%S", localtime())

    def input_text(self, el, text):
        el.clear()
        el.send_keys(text)
        return el

    def log(self, msg):
        print("[{}]{}".format(self.get_timestamp(), msg))

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
