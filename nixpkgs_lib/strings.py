"""strings module"""

from string import ascii_uppercase
from typing import Callable, List, Dict, Any

from nixpkgs_lib._curry import curry
from nixpkgs_lib.lists import imap1
from nixpkgs_lib.builtins import map_attrs, attr_values

upper_chars = ascii_uppercase


def to_upper(s: str) -> str:
    """Transform each character of the string to uppercase"""

    return s.upper()


def char_to_int(char: str) -> int:
    """Return the Unicode code point of a single-character string."""

    return ord(char)


@curry
def cmake_option_type(t: str, feature: str, value: str) -> str:
    """Build a CMake -D option string with the given type and value."""

    types = {"BOOL", "FILEPATH", "PATH", "STRING", "INTERNAL", "LIST"}

    t = t.upper()

    assert t in types

    return f"-D{feature}:{t}={value}"


@curry
def cmake_bool(condition: str, flag: bool) -> str:
    """Build a CMake BOOL -D option from a boolean flag."""

    flag_str = "TRUE" if flag else "FALSE"

    return cmake_option_type("BOOL", condition, flag_str)


@curry
def cmake_feature(condition: str, value: str) -> str:
    """Build a CMake STRING -D option for a feature and value."""

    return cmake_option_type("STRING", condition, value)


@curry
def common_prefix_length(a: str, b: str) -> int:
    """Return the length of the common prefix of two strings."""

    i = 0
    n, m = len(a), len(b)

    while i < n and i < m and a[i] == b[i]:
        i += 1

    return i


@curry
def common_suffix_length(a: str, b: str) -> int:
    """Return the length of the common suffix of two strings."""

    i, j = len(a) - 1, len(b) - 1

    ans = 0
    while i >= 0 and j >= 0 and a[i] == b[j]:
        i -= 1
        j -= 1
        ans += 1

    return ans


@curry
def concat_strings_sep(sep: str, lst: List[str]) -> str:
    """Join a list of strings using the given separator."""

    return sep.join(lst)


@curry
def concat_strings(lst: List[str]) -> str:
    """Concatenate a list of strings with no separator."""

    return concat_strings_sep("", lst)


@curry
def concat_lines(lst: List[str]) -> str:
    """Concatenate strings using newline separators."""

    return concat_strings_sep("\n", lst)


@curry
def concat_map_strings_sep(sep: str, f: Callable, lst: List[str]) -> str:
    """Map over strings then join them with the given separator."""

    return sep.join([f(el) for el in lst])


@curry
def concat_map_strings(f: Callable, lst: List[str]) -> str:
    """Map over strings then concatenate with no separator."""

    return concat_map_strings_sep("", f, lst)


@curry
def concat_imap_strings(f: Callable, lst: List[str]) -> str:
    """Concatenate results of index-aware mapping with no separator."""

    return concat_strings(imap1(f, lst))


@curry
def concat_imap_strings_sep(sep: str, f: Callable, lst: List[str]) -> str:
    """Join results of index-aware mapping with the given separator."""

    return concat_strings_sep(sep, imap1(f, lst))


@curry
def concat_map_attrs_string_sep(sep: str, f: Callable, attrs: Dict[str, Any]) -> str:
    """Join mapped attribute values with the given separator."""

    return concat_strings_sep(
        sep,
        attr_values(
            map_attrs(
                f,
                attrs,
            )
        ),
    )


@curry
def enable_feature(flag: bool, feature: str) -> str:
    flag_str = "enable" if flag else "disable"

    return f"--{flag_str}-{feature}"


@curry
def enable_feature_as(flag: bool, feature: str, value: str) -> str:
    ans = enable_feature(flag, feature)

    if flag:
        ans += f"={value}"

    return ans
