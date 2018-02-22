import abc

from tntestr import registry

class BaseScheduler(object, metaclass=abc.ABCMeta):
    name = None  # type: str
    registry = None  # type: registry.Registry
