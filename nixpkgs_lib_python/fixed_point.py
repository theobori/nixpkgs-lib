"""fixed point module"""

from typing import Callable, Iterator

from .laziness_simulation.lazy_iterator import LazyIterator


def fix(f: Callable) -> Iterator:
    # Evaluates with the stub value
    result = f(LazyIterator())
    # Final evaluation
    result = f(result)

    return result


def fix_prime(f: Callable) -> Iterator:
    result = fix(f)

    if type(result) is dict:
        result["__unfix__"] = f

    return result


def extends(overlay: Callable, f: Callable) -> Callable:
    def inner(final: dict) -> dict:
        prev = f(final)

        final = prev | overlay(final, prev)
        out = prev | overlay(final, prev)

        return out

    return inner
