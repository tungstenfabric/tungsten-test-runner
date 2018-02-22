import os

from typing import Tuple, List

from oslo_concurrency.processutils import execute
from typing import Set


class SconsBuildError(RuntimeError):
    pass


class SconsExecutor(object):
    """Abstracts SCons interactions to build targets required for tests"""

    def _execute_scons(self, arguments : List[str]) -> Tuple[bytes, bytes]:
        pass

    def rebuild_targets(self, targets: Set[str]) -> None:
        """

        :param targets: A set of SCons targets to execute
        :raises: SConsBuildError: if SCons build failed
        """

        env_copy = os.environ.copy()

        # Don't run any of the tests
        env_copy['BUILD_ONLY'] = 'True'
        # Use sparse compiler output
        env_copy['BUILD_QUIET'] = 'True'

        cmd = ["scons", "-j", "2", targets]

        try:
            execute(cmd, env_variables=env_copy)
        except RuntimeError as e:
            raise SconsBuildError(e)


    def get_test_targets(self):
        """Returns a list of test targets defined for the project.

        This method returns a list of all tests targets known to SCons.
        """
        arguments = ["--list-test-targets"]

