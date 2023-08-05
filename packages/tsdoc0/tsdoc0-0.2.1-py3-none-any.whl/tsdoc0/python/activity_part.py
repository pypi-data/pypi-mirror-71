from tsdoc0.python.model import Model
from tsdoc0.python.segment import Segment
from typing import Final
from typing import Optional

import attr


@attr.s(auto_attribs=True, kw_only=True)
class ActivityPart(Segment):
    parent: Optional[Model] = attr.ib(eq=False)
    number: Final[str]  # type: ignore[misc]

    @property
    def code(self) -> str:
        return f"Part {self.number}: "
