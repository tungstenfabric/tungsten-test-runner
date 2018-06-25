import voluptuous as vs
import logging
import yaml

from typing import Dict, List  # noqa

from tntestr import driver  # noqa
from tntestr import registry


class Scons(object):
    def __init__(self):
        self.targets = []

    @staticmethod
    def get_schema() -> vs.Schema:
        return vs.Schema({
            vs.Required("targets"): vs.All([str]),
        })


class Component(object):
    @staticmethod
    def get_schema():
        return vs.Schema(str)


class Module(object):
    def __init__(self):
        self.config_file : str = None
        self.line = 0
        self.name : str = None
        self.component : Component = None
        self.scons : Scons = None
        self.driver : driver.BaseDriver = None

    @staticmethod
    def get_schema(registry: registry.Registry) -> vs.Schema:
        drivers_schema = registry.get_driver_schemas()

        schema = {
            "name": str,
            vs.Required("component"): Component.get_schema(),
            vs.Required("scons"): Scons.get_schema(),
            vs.Required("driver"): drivers_schema,
        }
        return vs.Schema({vs.Required("module"): schema})


class TestLayoutParserError(Exception):
    pass


class TestLayout(object):
    """Hold a layout of all tests defined for the project"""

    def __init__(self, layout_yaml):
        self.log = logging.getLogger("tntestr.TestLayout")
        self.layout_yalm = layout_yaml

        self.modules : Dict[str, Module] = {}
        self.components : Dict[str, Component] = {}

    def extend_layout(self, config_file: str, layout_buf: str) -> None:
        """Add additional tests from YAML"""
        layout = yaml.safe_load(layout_buf)
        self.modules : List[Module] = None

        for item in layout:
            if len(item.keys()) > 1 or 'test' not in item:
                raise TestLayoutParserError("Does not conform to schema, item.keys() > 1 or 'test' not in item")

    def parse_layout(self) -> None:
        pass

    @staticmethod
    def get_schema(registry: registry.Registry) -> vs.Schema:
        module = Module.get_schema(registry)

        return vs.Schema(vs.All([module]))
