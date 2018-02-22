import logging
import voluptuous as vs
import os
import yaml

from tntestr.models.layout import TestLayout
from tntestr.repo import GitRepo
from tntestr.registry import Registry


class LayoutParser(object):
    def __init__(self, registry: Registry) -> None:
        self.log = logging.getLogger("testr.LayoutParser")
        self.layout = None  # type: TestLayout
        self.registry = registry

    def get_tests(self) -> TestLayout:
        repo = GitRepo()

        self.log.debug("Searching for test layout files within projects")
        for r in repo.repositories:
            layout_path = None  # type: str
            for fname in ['tests.yaml', '.tests.yaml']:
                path = os.path.join(r.path, fname)
                if os.path.exists(path):
                    self.log.debug("Test layout {} found", fname)
                    layout_path = path
                    break
            if not layout_path:
                self.log.debug("Test layout for {} missing.", r.name)
                continue
            self.parse_tests(layout_path)

    def parse_tests(self, layout_path: str) -> TestLayout:
        with open(layout_path, "r") as fh:
            layout = yaml.safe_load(fh)

        TestLayout.get_schema(self.registry)(layout)
