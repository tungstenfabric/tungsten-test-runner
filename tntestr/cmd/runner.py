import argparse
import logging

from tntestr.models.layout import TestLayout
from tntestr.parser import LayoutParser
from tntestr.registry import  Registry
from tntestr.scons import SconsExecutor
from tntestr.repo import GitRepo


class TestRunner(object):
    def parse_arguments(self) -> None:
        parser = argparse.ArgumentParser(
            description="Tungsten Fabric Test Runner")
        parser.add_argument("-c", dest="config", help="specify the config file")
        parser.add_argument("-v", "--verbose", dest="verbose", help="print the verbose output")
        parser.add_argument("--version", dest="version", help="show tntestr version")

        subparsers = parser.add_subparsers(title="commands",
                                           description="supported commands") # type: argparse._SubParsersAction
        cmd_test = subparsers.add_parser("test", help="run tests") # type: argparse.ArgumentParser
        cmd_test.add_argument("patterns", metavar='PATTERN', type=str, nargs='*',
                              help="a list of test patterns to operate on")
        cmd_test.add_argument("--list-tests", help="print a list of tests matching given patterns")
        cmd_test.add_argument("--filter", action="append", nargs=2, dest="filters",
                              help="filter tests by a regular expression")

    def __init__(self):
        self.log = logging.getLogger("tntestr.TestRunner")

        self.parse_arguments()

        registry = Registry()
        self.parser = LayoutParser()
        self.scheduler = registry.get_scheduler("Sequential")
        self.scheduler.registry = registry
        self.layout = self.parser.parse()


def main():
    runner = TestRunner()
    runner.parse_arguments()


if __name__ == "__main__":
    main()