"""stub module"""

from typing import Tuple, Any, Dict, Callable

from nixpkgs_lib.dunders import DUNDERS_ALL, DUNDERS_ORDER


def alu_stub_function(self, other: Any):
    """_summary_

    Args:
        other (Any): _description_

    Returns:
        _type_: _description_
    """

    return other


def do_stub_calls(dunders: Tuple[str], stub_function: Callable):
    """_summary_

    Args:
        dunders (Tuple[str]): _description_
        stub_function (Callable): _description_

    Returns:
        _type_: _description_
    """

    return {name: stub_function for name in dunders}


ALU_DUNDER_CALLS = do_stub_calls(DUNDERS_ALL, alu_stub_function)
DUNDERS_ORDER_CALLS = do_stub_calls(DUNDERS_ORDER, alu_stub_function)
TYPES_DUNDERS_CALLS = {
    "__str__": lambda _: str(),
    "__bool__": lambda _: bool(),
    "__int__": lambda _: int(),
    "__float__": lambda _: float(),
    "__bytes__": lambda _: bytes(),
    "__repr__": lambda _: str(),
}


METHODS_CALLS = {
    **ALU_DUNDER_CALLS,
    **DUNDERS_ORDER_CALLS,
    **TYPES_DUNDERS_CALLS,
}


class StubMeta(type):
    """Stub metaclass, mainly used to initialize dunders methods during
    class build time

    Args:
        type (_type_): _description_
    """

    def __new__(cls, name: str, bases: Tuple[type, ...], namespace: Dict[str, Any]):
        for name, stub_function in METHODS_CALLS.items():
            namespace[name] = stub_function

        return super().__new__(cls, name, bases, namespace)


class Stub(metaclass=StubMeta):
    """Short lifetime object used as a stub for function
    that needs laziness simulation

    Args:
        metaclass (_type_, optional): _description_. Defaults to StubMeta.
    """

    def __getitem__(self, key: Any):
        return Stub()
