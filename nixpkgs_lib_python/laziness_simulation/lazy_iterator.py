"""lazy iterator module"""

from typing import Tuple, Dict, Any

from .stub import Stub


class LazyIterator(list):
    """Lazy iterator object, it is supposed to have a short
    lifetime

    Args:
        list (_type_): _description_
    """

    def __init__(self, *args: Tuple[Any], **kwargs: Dict[str, Any]):
        self.__memo = {}

    def __getitem__(self, key):
        if key in self.__memo:
            return self.__memo[key]

        value = Stub()
        self.__memo[key] = value

        return value
