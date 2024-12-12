"""lists module"""

import re
import functools

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


def last(lst: list) -> Any:
    """Return the last element of a list"""

    assert len(lst) > 0
    return lst[-1]


def tail(lst: list) -> Any:
    """Return all elements of the list except the first"""

    assert len(lst) > 0
    return lst[1:]


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
def find_first_index(pred: Callable, default: Any, lst: list) -> Any:
    """Find first element matching predicate or return default"""

    for i, x in enumerate(lst):
        if pred(x) is True:
            return i

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


@curry
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


@curry
def has_prefix(list1: list, list2: list) -> bool:
    """Whether the first list is a prefix of the second list"""

    return list1 == list2[: len(list1)]


@curry
def remove_prefix(list1: list, list2: list) -> list:
    """Remove the first list as a prefix from the second list"""

    if not has_prefix(list1, list2):
        raise ValueError("First argument is not a prefix of the second argument")

    return list2[len(list1) :]


@curry
def sublist(start: int, count: int, lst: list) -> list:
    """Return a sublist of count elements starting at start"""

    length = len(lst)
    if start >= length:
        return []

    end = min(start + count, length)
    return lst[start:end]


@curry
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


@curry
def mutually_exclusive(a: list, b: list) -> bool:
    """Test if two lists have no common elements"""

    return len(a) == 0 or not any(x in a for x in b)


@curry
def drop(count: int, lst: list) -> list:
    """Drop count elements from the beginning of the list"""

    return lst[count:]


@curry
def elem(x: Any, xs: list) -> bool:
    """Return true if x is an element of xs"""

    return x in xs


@curry
def __seq(_e1: Any, e2: Any) -> Any:
    """Return second argument"""

    return e2


@curry
def __foldl_prime(op: Callable, nul: Any, lst: list) -> Any:
    """Left fold with accumulator"""

    _len = len(lst)

    def inner(n: int):
        if n < 0:
            return nul

        return op(inner(n - 1))(lst[n])

    return inner(_len - 1)


@curry
def foldl_prime(op: Callable, acc: Any) -> Any:
    """Left fold with initial accumulator"""

    return __seq(acc)(__foldl_prime(op)(acc))


@curry
def count(pred: Callable) -> Callable:
    """Count how many elements satisfy the predicate"""

    f = lambda c: lambda x: c + 1 if pred(x) else c

    return foldl_prime(f)(0)


@curry
def elem_at(xs: list, n: int) -> Any:
    """Return nth element of the list"""

    return xs[n]


@curry
def _filter(f: Callable, lst: list) -> list:
    """Filter list elements using predicate"""

    return list(filter(f, lst))


def is_list(e: Any) -> bool:
    """Return true if argument is a list"""

    return type(e) is list


def length(lst: list) -> int:
    """Return the length of the list"""

    return len(lst)


@curry
def _map(f: Callable, lst: list) -> list:
    """Map function over list elements"""

    return list(map(f, lst))


@curry
def optional(cond: bool, elem: Any) -> list:
    """Return singleton list if condition is true, empty list otherwise"""

    return [elem] if cond is True else []


@curry
def optionals(cond: bool, elem: Any) -> list:
    """Return list if condition is true, empty list otherwise"""

    return elem if cond is True else []


def take(count: int) -> Callable:
    """Take first count elements from list"""

    return sublist(0)(count)


def unique(lst: list) -> list:
    """Remove duplicate elements from list"""

    f = lambda acc: lambda e: acc if elem(e)(acc) else acc + [e]

    return foldl_prime(f)([])(lst)


@curry
def sort(comparator: Callable, lst: list) -> list:
    """Sort list using comparator function"""

    f = lambda a, b: comparator(a)(b)
    f = functools.cmp_to_key(f)

    return sorted(lst, key=f)


def to_list(x: Any) -> list:
    """Convert argument to list if it isn't already"""

    return x if is_list(x) else [x]


def concat_lists(lst: list) -> list:
    """Concatenate a list of lists"""

    out = []

    for elem in lst:
        assert is_list(elem)

        out.extend(elem)

    return out


@curry
def concat_map(f: Callable, lst: list) -> list:
    """Map function and concatenate results"""

    return concat_lists(_map(f)(lst))


def cross_lists(f: Callable) -> Callable:
    """Generate cross product of lists"""

    ff = lambda fs: lambda args: concat_map(lambda f: _map(f)(args))(fs)

    return foldl(ff)([f])


@curry
def gen_list(generator: Callable, length: int) -> list:
    """Generate list using function and length"""

    return [generator(i) for i in range(length)]


@curry
def list_dfs(stop_on_cycles: bool, before: Callable, lst: list) -> dict:
    """Perform depth-first search on a list with cycle detection"""

    @curry
    def dfs_prime(us: Any, visited: list, rest: list) -> dict:
        c = _filter(lambda x: before(x)(us))(visited)
        if stop_on_cycles is True and length(c) > 0:
            return {
                "cycle": us,
                "loops": c,
                "visited": visited,
                "rest": rest,
            }

        b = partition(lambda x: before(x)(us))(rest)
        if length(b["right"]) == 0:
            return {
                "minimal": us,
                "visited": visited,
                "rest": rest,
            }

        return dfs_prime(head(b["right"]))([us] + visited)(
            tail(b["right"]) + b["wrong"]
        )

    return dfs_prime(head(lst))([])(tail(lst))


@curry
def toposort(before: Callable, lst: list) -> dict:
    """Topologically sort a list using the given ordering function"""

    if length(lst) < 2:
        return {"result": lst}

    dfs_this = list_dfs(True)(before)(lst)
    if "cycle" in dfs_this:
        return {
            "cycle": reverse_list([dfs_this["cycle"]] + dfs_this["visited"]),
            "loops": dfs_this["loops"],
        }

    toporest = toposort(before)(dfs_this["visited"] + dfs_this["rest"])
    if "cycle" in toporest:
        return toporest

    return {"result": [dfs_this["minimal"]] + toporest["result"]}
