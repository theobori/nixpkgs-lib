"""curry module"""

from typing import Callable, Tuple


def curry(func: Callable):
    """Decorator used to 'currify' a standard Python function

    See https://en.wikipedia.org/wiki/Currying
    See https://python-course.eu/advanced-python/currying-in-python.php

    Args:
        func (_type_): _description_
    """

    def curried(*args: Tuple[str]):
        if len(args) == func.__code__.co_argcount:
            return func(*args)

        return lambda x: curried(*(args + (x,)))

    return curried
