"""lists module"""

import re

from typing import Callable, Any, List, Iterator

from .curry.curry import curry


@curry
def foldr(op: Callable, nul: Any, lst: list) -> Any:
    """Fold a list from right to left using a binary operator"""

    _len = len(lst)

    def fold_prime(n: int):
        if n == _len:
            return nul

        return op(lst[n])(fold_prime(n + 1))

    return fold_prime(0)


fold = foldr


@curry
def for_each(xs: Iterator, f: Callable) -> Iterator:
    """Apply a function to each element in an iterator"""

    return map(f, xs)


def singleton(x: Any) -> list:
    """Create a single-element list containing the given value"""

    return [x]


@curry
def foldl(op: Callable, nul: Any, lst: list) -> Any:
    """Fold a list from left to right using a binary operator"""

    _len = len(lst)

    def fold_prime(n: int):
        if n < 0:
            return nul

        return op(fold_prime(n - 1))(lst[n])

    return fold_prime(_len - 1)


@curry
def _all(pred: Callable, lst: list) -> bool:
    """Test if all elements in list satisfy the predicate"""

    return all(map(pred, lst))


@curry
def all_unique(lst: list) -> bool:
    """Check if all elements in the list are unique"""

    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i] == lst[j]:
                return False

    return True


def head(lst: list) -> Any:
    """Return the first element of a list"""

    assert len(lst) > 0
    return lst[0]


def tail(lst: list) -> Any:
    """Return the last element of a list"""

    assert len(lst) > 0
    return lst[-1]


@curry
def _any(pred: Callable, lst: list) -> bool:
    """Test if any element in list satisfies the predicate"""

    return any(map(pred, lst))


@curry
def imap0(f: Callable, lst: list) -> list:
    """Map a function over list elements with their 0-based indices"""

    return list(map(lambda i: f(i)(lst[i]), range(len(lst))))


@curry
def imap1(f: Callable, lst: list) -> list:
    """Map a function over list elements with their 1-based indices"""

    return list(map(lambda i: f(i + 1)(lst[i]), range(len(lst))))


@curry
def ifilter0(ipred: Callable, lst: list) -> list:
    """Filter list elements using a predicate that takes both index and value"""

    return [x for i, x in enumerate(lst) if ipred(i)(x) is True]


def flatten(x: Any) -> list:
    """Recursively flatten nested lists into a single list"""

    if isinstance(x, list):
        return [item for sublist in x for item in flatten(sublist)]

    return [x]


@curry
def remove(e: Any, lst: list) -> list:
    """Remove all occurrences of an element from a list"""

    return list(filter(lambda x: x != e, lst))


@curry
def find_single(pred: Callable, default: Any, multiple: Any, lst: list) -> Any:
    """Find single element matching predicate, handle no/multiple matches"""

    matches = list(filter(lambda x: pred(x), lst))

    if len(matches) == 0:
        return default
    if len(matches) == 1:
        return matches[0]

    return multiple


@curry
def find_first(pred: Callable, default: Any, lst: list) -> Any:
    """Find first element matching predicate or return default"""

    for x in lst:
        if pred(x) is True:
            return x

    return default


@curry
def _range(first: int, last: int) -> list:
    """Return a list of integers from first up to and including last"""
    return [] if first > last else list(range(first, last + 1))


@curry
def replicate(n: int, elem: Any) -> list:
    """Return a list with n copies of an element"""
    return [elem] * n


@curry
def partition(pred: Callable, lst: list) -> dict:
    """Split elements into two lists based on predicate"""

    right = []
    wrong = []

    for x in lst:
        if pred(x):
            right.append(x)
        else:
            wrong.append(x)

    return {"right": right, "wrong": wrong}


@curry
def group_by(pred: Callable, lst: list) -> dict:
    """Group list elements by predicate result as key"""

    result = {}

    for x in lst:
        key = pred(x)
        if key not in result:
            result[key] = []

        result[key].append(x)

    return result


@curry
def group_by_prime(op: Callable, nul: Any, pred: Callable, lst: list) -> dict:
    """Group elements by predicate with custom combining operation"""

    result = {}

    for x in lst:
        key = pred(x)
        if key not in result:
            result[key] = nul

        result[key] = op(result[key], x)

    return result


@curry
def zip_lists_with(f: Callable, fst: list, snd: list) -> list:
    """Merge two lists using a function"""

    return [f(a, b) for a, b in zip(fst, snd)]


def zip_lists(fst: list, snd: list) -> list:
    """Merge two lists into list of pairs"""

    return [{"fst": a, "snd": b} for a, b in zip(fst, snd)]


def reverse_list(xs: list) -> list:
    """Reverse the order of list elements"""

    return list(reversed(xs))


@curry
def compare_lists(cmp: Callable, a: list, b: list) -> int:
    """Compare two lists element-by-element"""

    if not a:
        return 0 if not b else -1

    if not b:
        return 1

    rel = cmp(a[0], b[0])
    if rel == 0:
        return compare_lists(cmp, a[1:], b[1:])

    return rel


def natural_sort(lst: list) -> list:
    """Sort list using natural sorting"""

    def vectorize(s):
        parts = re.split(r"(0|[1-9][0-9]*)", str(s))
        return [int(x) if x.isdigit() else x for x in parts]

    return sorted(lst, key=vectorize)


def has_prefix(list1: list, list2: list) -> bool:
    """Whether the first list is a prefix of the second list"""

    return list1 == list2[: len(list1)]


def remove_prefix(list1: list, list2: list) -> list:
    """Remove the first list as a prefix from the second list"""

    if not has_prefix(list1, list2):
        raise ValueError("First argument is not a prefix of the second argument")

    return list2[len(list1) :]


def sublist(start: int, count: int, lst: list) -> list:
    """Return a sublist of count elements starting at start"""

    length = len(lst)
    if start >= length:
        return []

    end = min(start + count, length)
    return lst[start:end]


def common_prefix(list1: list, list2: list) -> list:
    """Find the common prefix of two lists"""

    common = []

    for a, b in zip(list1, list2):
        if a != b:
            break

        common.append(a)

    return common


def init(lst: list) -> list:
    """Return all elements but the last"""

    if not lst:
        raise ValueError("init: list must not be empty!")

    return lst[:-1]


@curry
def intersect_lists(list1: list, list2: list) -> list:
    """Return elements present in both lists"""

    return [x for x in list2 if x in list1]


@curry
def subtract_lists(list1: list, list2: list) -> list:
    """Remove elements of first list from second list"""

    return [x for x in list2 if x not in list1]


def mutually_exclusive(a: list, b: list) -> bool:
    """Test if two lists have no common elements"""

    return len(a) == 0 or not any(x in a for x in b)
