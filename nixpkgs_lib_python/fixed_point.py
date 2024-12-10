"""fixed point module"""

from typing import Callable, Iterator, Any

from .laziness_simulation.lazy_iterator import LazyIterator
from .curry.curry import curry


def fix(f: Callable) -> Iterator:
    """Compute the least fixed point of a function"""

    # Evaluates with the stub value
    result = f(LazyIterator())
    # Final evaluation
    result = f(result)

    return result


def fix_prime(f: Callable) -> Iterator:
    """Like fix but preserves the original function in __unfix__"""

    result = fix(f)

    if type(result) is dict:
        result["__unfix__"] = f

    return result


@curry
def extends(overlay: Callable, f: Callable) -> Callable:
    """Create a new fixed point with an overlay applied to the previous one"""

    def inner(final: dict) -> dict:
        prev = f(final)

        final = prev | overlay(final)(prev)
        out = prev | overlay(final)(prev)

        return out

    return inner


@curry
def converge(f: Callable, x: Any) -> Any:
    """Apply function f repeatedly until it converges to a fixed point"""

    x_prime = f(x)

    if x_prime == x:
        return x

    return converge(f, x_prime)


def to_extension(f: Any) -> Any:
    """Convert a function to an extension compatible form"""

    if callable(f) is False:
        return lambda final: lambda prev: f

    @curry
    def inner(final, prev):
        f_prev = f(prev)

        if callable(f_prev) is True:
            return f(final)(prev)

        return f_prev

    return inner
