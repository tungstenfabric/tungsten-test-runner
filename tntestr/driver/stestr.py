import logging
import subunit

from stestr import scheduler as stestr_sched
from typing import List, Optional, Set


from tntestr import scheduler as scheduler
from tntestr.driver import BaseDriver


class StestrDriver(BaseDriver):
    name = "stestr"

    def __init__(self):
        self.log = logging.getLogger("driver.StestrDriver")

    def execute_tests(self, test_list: Optional[Set] = None):
        pass

    def get_failing(self):
        pass

    def get_last_result(self, display_tests: bool):
        pass

    @classmethod
    def get_schema(cls):
        pass
