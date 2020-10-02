import logging

from aio_wx_widgets.sizers import AlignHorizontal
from aio_wx_widgets.widgets.grid import Grid
from aio_wx_widgets.widgets.text import Text

_LOGGER = logging.getLogger(__name__)


class LabelledItem(Grid):
    def __init__(self, label_text: str, item, align_right=True):
        super().__init__()
        self.label_text = label_text
        self._item = item
        self.align_right = align_right

    def __call__(self, parent, *args, **kwargs):
        super().__call__(parent)
        if self.align_right:
            alignment = AlignHorizontal.right
        else:
            alignment = None
        self.add(
            Text(self.label_text),
            margin=(4, 4, 5, 1),
            weight=4,
            align_horizontal=alignment,
        )
        self.add(self._item, weight=4)

        return self
