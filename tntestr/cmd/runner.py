import argparse
import logging
import logging.config

from tntestr.models.layout import TestLayout
from tntestr.parser import LayoutParser
from tntestr.registry import  Registry
from tntestr.scons import SconsExecutor
from tntestr.repo import GitRepo


class TestRunner(object):
    def parse_arguments(self) -> None:
        parser = argparse.ArgumentParser(
            description="Tungsten Fabric Test Runner")
        parser.add_argument("--debug", dest="debug", action="store_true")
        parser.add_argument("-c", dest="config", help="specify the config file")
        parser.add_argument("--version", dest="version", help="show tntestr version")

        subparsers = parser.add_subparsers(title="commands", description="supported commands")
        cmd_test : argparse.ArgumentParser = subparsers.add_parser("test", help="run tests")
        cmd_test.add_argument("patterns", metavar='PATTERN', type=str, nargs='*',
                              help="a list of test patterns to operate on")
        cmd_test.add_argument("--list-tests", help="print a list of tests matching given patterns")
        cmd_test.add_argument("--filter", action="append", nargs='+', dest="filters",
                              help="filter tests by a regular expression")

        self.args = parser.parse_args()

    def __init__(self):
        self.log = logging.getLogger("tntestr.TestRunner")

    def parse_layout(self):
        registry = Registry()
        self.parser = LayoutParser(registry)
        self.layout = self.parser.parse()

    def setup_logging(self):
        log_config = {
            "version": 1,
            'disable_existing_loggers': True,
            "formatters": {
                'detailed': {
                    'format': '%(asctime)s %(name)s %(levelname)s\t%(message)s'
                },
                'simple': {
                    "format": "%(message)s"
                }
            },
            "handlers": {
                'console': {
                    'class': 'logging.StreamHandler',
                    "formatter": "simple",
                    'level': "DEBUG" if self.args.debug else "INFO",
                },
            },
            "root": {
                "level": "DEBUG",
                "handlers": ["console"],
                "propagate": "1"
            }
        }
        logging.config.dictConfig(log_config)
        self.log = logging.getLogger("PublisherApp")

    def execute(self):
        """
        1. Gather tests based on filters and generate scons targets to execute
        2. Run scons to build tests
        3. Run all tests defined in test_suites
        """

def main():
    runner = TestRunner()
    runner.parse_arguments()
    runner.setup_logging()
    runner.execute()

if __name__ == "__main__":
    main()
