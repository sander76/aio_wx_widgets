import logging

from aio_wx_widgets.core.data_types import HorAlign, VerAlign
from aio_wx_widgets.containers.grid import Grid
from aio_wx_widgets.widgets.text import Text

_LOGGER = logging.getLogger(__name__)

__all__ = ["LabelledItem"]


class LabelledItem(Grid):
    def __init__(
        self, label_text: str, item, align_right=True, label_weight=1, item_weight=1
    ):
        super().__init__()
        self.label_text = label_text
        self._item = item
        self._label_weight = label_weight
        self._item_weight = item_weight
        self.align_right = align_right

    def __call__(self, parent, *args, **kwargs):
        super().__call__(parent)
        if self.align_right:
            hor_alignment = HorAlign.right
        else:
            hor_alignment = None
        self.add(
            Text(self.label_text),
            weight=self._label_weight,
            hor_align=hor_alignment,
            ver_align=VerAlign.center,
        )
        self.add(self._item, weight=self._item_weight)

        return self
