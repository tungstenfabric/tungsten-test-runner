import logging
import voluptuous as vs
import os
import yaml

from typing import List

from tntestr.models.layout import TestLayout
from tntestr.repo import GitRepo
from tntestr.registry import Registry


class LayoutParser(object):
    def __init__(self, registry: Registry) -> None:
        self.log = logging.getLogger("testr.LayoutParser")
        self.layout : TestLayout = None
        self.registry = registry

    def get_tests(self, test_layouts : List[str]) -> TestLayout:
        self.log.debug("Searching for test layout files within projects")
        for layout_path in test_layouts:
            self.parse_tests(layout_path)

    def parse_tests(self, layout_path: str) -> TestLayout:
        with open(layout_path, "r") as fh:
            layout = yaml.safe_load(fh)

        TestLayout.get_schema(self.registry)(layout)

    def parse(self):
        pass
