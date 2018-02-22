import logging

from typing import List, Optional, Set

from tntestr.driver import BaseDriver


class ToxRunner(BaseDriver):
    name = "tox"

    def __init__(self):
        self.log = logging.getLogger("driver.ToxRunner")

    def discover_tests(self) -> List:
        pass

    def execute_tests(self, test_list: Optional[Set] = None):
        pass

    def get_failing(self):
        pass

    def get_last_result(self, display_tests: bool):
        pass

    @classmethod
    def get_schema(cls):
        pass
