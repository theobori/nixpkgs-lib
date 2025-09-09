"""stub sequence module"""

from typing import Any, Sequence

from nixpkgs_lib.laziness_simulation.stub import Stub


class StubSequence(list):
    """Stub sequence object, it is supposed to have a short
    lifetime
    """

    def __getitem__(self, _: Any):
        return Stub()
