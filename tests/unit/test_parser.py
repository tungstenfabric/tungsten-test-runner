import voluptuous as vs

from typing import List, Optional, Set

from unittest import TestCase

from tntestr import driver
from tntestr import registry
from tntestr import parser

from tntestr.driver import gtest


class FakeDriver(driver.BaseDriver):
    name = "fake1"

    def discover_tests(self) -> List:
        return []

    def execute_tests(self, test_list: Optional[Set] = None) -> None:
        pass

    def get_failing(self) -> None:
        pass

    def get_last_result(self, display_tests: bool) -> None:
        pass

    @classmethod
    def get_schema(cls) -> vs.Schema:
        return vs.Schema({})


class TestLayoutParser(TestCase):
    def setUp(self):
        self.registry = registry.Registry()
        self.registry.register_driver(FakeDriver())
        self.registry.register_driver(gtest.GTestDriver)
        self.parser = parser.LayoutParser(self.registry)

    def test_parse_minimal_schema(self):
        self.parser.parse_tests("tests/fixtures/layouts/simple.yaml")

    def test_parse_spec_schema(self):
        self.parser.parse_tests("tests/fixtures/layouts/spec-layout.yaml")
