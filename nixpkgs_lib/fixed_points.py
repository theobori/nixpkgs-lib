"""fixed point module"""

from typing import Callable, Sequence, Any

from nixpkgs_lib.laziness_simulation import StubSequence
from nixpkgs_lib.curry import curry
from nixpkgs_lib.lists import foldr


def fix(f: Callable) -> Sequence:
    """Compute the least fixed point of a function"""

    # Evaluates with the stub value
    result = f(StubSequence())
    # Final evaluation
    result = f(result)

    return result


def fix_prime(f: Callable) -> Sequence:
    """Like fix but preserves the original function in __unfix__"""

    result = fix(f)

    if isinstance(result, dict):
        result["__unfix__"] = f

    return result


@curry
def extends(overlay: Callable, f: Callable) -> Callable:
    """Extend a fixed point with an overlay function"""

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
    """Convert a function to an extension-compatible form"""

    if callable(f) is False:
        return lambda final: lambda prev: f

    @curry
    def inner(final, prev):
        f_prev = f(prev)

        if callable(f_prev) is True:
            return f(final)(prev)

        return f_prev

    return inner


@curry
def compose_extensions(f: Callable, g: Callable, final: dict, prev: dict) -> Any:
    """Compose two extensions into a single extension"""

    f_applied = f(final)(prev)
    prev_prime = prev | f_applied

    return f_applied | g(final)(prev_prime)


compose_many_extensions = foldr(lambda x: lambda y: compose_extensions(x)(y))(
    lambda final: lambda prev: {}
)


@curry
def make_extensible_with_custom_name(extender_name: str, rattrs: Callable) -> dict:
    """Make a fixed-point with a custom name for the extension function"""

    def inner(self: dict) -> dict:
        func = lambda f: make_extensible_with_custom_name(extender_name)(
            extends(f)(rattrs)
        )

        return rattrs(self) | {extender_name: func}

    return fix_prime(inner)


def make_extensible(rattrs: Callable) -> dict:
    """Make a fixed-point with the default "extend" function name"""

    return make_extensible_with_custom_name("extend")(rattrs)
