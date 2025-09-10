"""builtin module"""

import builtins

from typing import List


def filter_attributes(names: List[str]) -> List[str]:
    """Filter Python attributes, keeping only snake_case string

    Args:
        names (List[str]): Attributes

    Returns:
        List[str]: Filtered attributes
    """

    return list(
        filter(
            lambda name: not (
                (name.startswith("__") and name.endswith("__")) or name[0].isupper()
            ),
            names,
        )
    )


_BUILTIN_NAMES = dir(builtins)
BUILTIN_NAMES = set(_BUILTIN_NAMES)
BUILTIN_NAMES_FILTERED = set(filter_attributes(_BUILTIN_NAMES))
