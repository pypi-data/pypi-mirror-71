from textx.model import get_model
from typing import cast
from typing import Tuple


class Positionable:
    @property
    def linecol(self) -> Tuple[int, int]:
        # Silence the error about a missing attribute because it already exists inside
        # of all textX model classes
        tx_position = self._tx_position  # type: ignore[attr-defined]

        return cast(
            Tuple[int, int], get_model(self)._tx_parser.pos_to_linecol(tx_position),
        )

    @property
    def line(self) -> int:
        return self.linecol[0]

    @property
    def column(self) -> int:
        return self.linecol[1]
