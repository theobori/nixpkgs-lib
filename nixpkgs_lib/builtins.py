"""In this module, only the necessary built-in features should be implemented"""

from typing import Callable, Dict, Any, List

from nixpkgs_lib._curry import curry


@curry
def map_attrs(f: Callable, attrset: Dict[str, Any]) -> Dict[str, Any]:
    return {name: f(name, value) for name, value in attrset.items()}


def attr_values(attrset: Dict[str, Any]) -> List[Any]:
    return list(attrset.values())
