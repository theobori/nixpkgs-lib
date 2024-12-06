"""fixed point module"""

from typing import Callable, Iterator, Any

from .laziness_simulation.lazy_iterator import LazyIterator
from .curry.curry import curry


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


@curry
def extends(overlay: Callable, f: Callable) -> Callable:
    def inner(final: dict) -> dict:
        prev = f(final)

        final = prev | overlay(final)(prev)
        out = prev | overlay(final)(prev)

        return out

    return inner


@curry
def converge(f: Callable, x: Any) -> Any:
    x_prime = f(x)

    if x_prime == x:
        return x

    return converge(f, x_prime)


def to_extension(f: Any) -> Any:
    if callable(f) is False:
        return lambda final: lambda prev: f

    @curry
    def inner(final, prev):
        f_prev = f(prev)

        if callable(f_prev) is True:
            return f(final)(prev)

        return f_prev

    return inner
