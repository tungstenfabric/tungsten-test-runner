import voluptuous as vs

from typing import List, Set

from tntestr.driver import BaseDriver, regex_or_str

class TestOverride(object):
    @staticmethod
    def get_schema():
        return vs.Schema({
            vs.Required("file_matchers"): vs.All([regex_or_str()]),
            vs.Optional("test_matchers"): vs.All([regex_or_str()]),
            vs.Optional("disabled"): bool,
            vs.Optional("flaky"): {
                vs.Required("strategy"): str
            },
        })

class GTestDriver(BaseDriver):
    name = "gtest"

    def discover_tests(self) -> List:
        pass

    def execute_tests(self, test_list: Set = None) -> None:
        pass

    def get_failing(self) -> None:
        pass

    def get_last_result(self, display_tests: bool) -> None:
        pass

    @classmethod
    def get_schema(cls):
        return vs.Schema({
            vs.Required("parallel"): bool,
            vs.Optional("test_suites"): vs.All([regex_or_str()]),
            vs.Optional("test_overrides"): vs.All([TestOverride.get_schema()]),
        })
