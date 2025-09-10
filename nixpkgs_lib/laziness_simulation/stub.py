"""stub module"""

from typing import Tuple, Any, Dict, Callable

from nixpkgs_lib._dunders import DUNDERS_ALL, DUNDERS_ORDER


def alu_stub_function(_: object, other: Any) -> Any:
    """Returns a stub value for ALU Python functions.

    Args:
        other (Any): _description_

    Returns:
        _type_: _description_
    """

    return other


def do_stub_calls(dunders: Tuple[str], stub_function: Callable) -> Dict[str, Callable]:
    """Associates Python special methods names with a stub function reference.

    Args:
        dunders (Tuple[str]): The names.
        stub_function (Callable): The stub function.

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
    """

    def __new__(cls, name: str, bases: Tuple[type, ...], namespace: Dict[str, Any]):
        for name, stub_function in METHODS_CALLS.items():
            namespace[name] = stub_function

        return super().__new__(cls, name, bases, namespace)


class Stub(metaclass=StubMeta):
    """Short lifetime object used as a stub for function
    that needs laziness simulation
    """

    def __getitem__(self, _: Any):
        return Stub()
