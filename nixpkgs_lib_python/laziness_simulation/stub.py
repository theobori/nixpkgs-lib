"""stub module"""

from typing import Tuple, Any, Dict, Callable

from ..dunders.dunders import ALU_DUNDERS, ORDER_DUNDERS


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


ALU_DUNDER_CALLS = do_stub_calls(ALU_DUNDERS, alu_stub_function)
ORDER_DUNDERS_CALLS = do_stub_calls(ORDER_DUNDERS, alu_stub_function)
TYPES_DUNDERS_CALLS = {
    "__str__": lambda self: str(),
    "__bool__": lambda self: bool(),
    "__int__": lambda self: int(),
    "__float__": lambda self: float(),
    "__bytes__": lambda self: bytes(),
    "__repr__": lambda self: str(),
}


METHODS_CALLS = {
    **ALU_DUNDER_CALLS,
    **ORDER_DUNDERS_CALLS,
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
