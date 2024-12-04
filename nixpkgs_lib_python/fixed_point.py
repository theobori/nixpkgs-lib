"""fixed point module"""

from .laziness_simulation.lazy_iterator import LazyIterator


def fix(f):
    # Evaluates with the stub value
    result = f(LazyIterator())
    # Final evaluation
    result = f(result)

    return result


def fix_prime(f):
    result = fix(f)

    if type(result) is dict:
        result["__unfix__"] = f

    return result
