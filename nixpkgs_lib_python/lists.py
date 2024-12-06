"""lists module"""

from typing import Callable, Any, List, Iterator

from .curry.curry import curry


@curry
def foldr(op: Callable, nul: Any, _list: List[Any]) -> Any:
    _len = len(_list)

    def fold_prime(n: int):
        if n == _len:
            return nul

        return op(_list[n])(fold_prime(n + 1))

    return fold_prime(0)


fold = foldr


@curry
def for_each(xs: Iterator, f: Callable) -> Iterator:
    return map(f, xs)
