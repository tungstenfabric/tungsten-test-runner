import abc
import voluptuous as vs


from typing import List, Set, Optional


def regex_or_str():
    def wrapped(value):
        if not isinstance(value, str):
            raise vs.Invalid("A valid string or a regular expression is required")

        if value[0] == "^" or value[-1] == "$":
            if value[0] != "^" or value[-1] != "$":
                raise vs.Invalid("Regular expression must start with ^ and end with $")

        return True
    return wrapped


class BaseDriver(object, metaclass=abc.ABCMeta):
    """Driver abstracts the unittest driver used for the given component
    providing a common set of APIs to control how tests are executed.
    """
    name = None  # type: str

    @abc.abstractmethod
    def discover_tests(self) -> List:
        """Discovers possible tests to be executed for the given target"""

    @abc.abstractmethod
    def execute_tests(self, test_list: Optional[Set] = None) -> None:
        pass

    @abc.abstractmethod
    def get_failing(self) -> None:
        pass

    @abc.abstractmethod
    def get_last_result(self, display_tests: bool) -> None:
        pass

    @classmethod
    @abc.abstractmethod
    def get_schema(cls) -> vs.Schema:
        pass
