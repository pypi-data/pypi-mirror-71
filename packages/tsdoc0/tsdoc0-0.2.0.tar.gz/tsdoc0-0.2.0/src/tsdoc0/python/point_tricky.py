from tsdoc0.python.model import Model
from tsdoc0.python.segment import Segment
from typing import Final
from typing import Optional

import attr


@attr.s(auto_attribs=True, kw_only=True)
class PointTricky(Segment):
    parent: Optional[Model] = attr.ib(eq=False)
    indentation: Final[str]  # type: ignore[misc]
    point: Final[str]  # type: ignore[misc]
    explanation: Final[str]  # type: ignore[misc]
