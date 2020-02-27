from time import sleep
from typing import Callable


class Pending:

    @property
    def timeout(self):
        return self.__timeout

    @timeout.setter
    def timeout(self, value):
        self.__timeout = value

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, value):
        self.__interval = value

    def __init__(self, timeout: int = None, interval: int = 1):
        self.timeout = timeout
        self.interval = interval

    def judge(self, assertion, error_value=False):
        try:
            return assertion()
        except:
            return error_value

    def until(self, assertion: Callable[[], bool]):
        count = 0
        while True:
            if self.judge(assertion):
                return self
            else:
                if self.timeout is not None and count * self.interval > self.timeout:
                    break
                else:
                    sleep(self.interval)
                    count += 1
        raise Exception("Timeout {} has reached".format(self.timeout))
