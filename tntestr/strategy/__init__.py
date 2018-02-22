import abc


class BaseStrategy(object, metaclass=abc.ABCMeta):
    name = None  # type: str


class Pass2of3(BaseStrategy):
    name = 'Pass2of3'

    runs = 3
    pass_threshold = 2
