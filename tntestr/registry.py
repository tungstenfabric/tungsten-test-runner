import logging
import voluptuous as vs
import typing

from typing import Dict  # noqa

from tntestr import driver
from tntestr import strategy


class Registry(object):
    """A registry of available schedulers, drivers and test strategies"""
    log = logging.getLogger("tntestr.Registry")

    def __init__(self):
        self.drivers : Dict[str, typing.Type[driver.BaseDriver]] = {}
        self.strategies : Dict[str, typing.Type[strategy.BaseStrategy]] = {}

    def register_driver(self, driver_obj: typing.Type[driver.BaseDriver]):
        if driver_obj.name in self.drivers:
            raise Exception("Driver {} already registered.", driver_obj.name)
        self.drivers[driver_obj.name] = driver_obj

    def register_strategy(self, strategy_obj: typing.Type[strategy.BaseStrategy]):
        if strategy_obj.name in self.strategies:
            raise Exception("Strategy {} already registered.", strategy_obj.name)
        self.strategies[strategy_obj.name] = strategy_obj

    def get_driver_schemas(self) -> vs.Schema:
        schema = {}
        single_driver = "There can be only one test runner driver for every module"

        for driver_name, driver_obj in self.drivers.items():
            schema.update({
                vs.Exclusive(driver_name, 'driver', single_driver): driver_obj.get_schema()
            })
        return vs.Schema(schema)
