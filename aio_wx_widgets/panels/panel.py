"""Panel. Sits in a frame. Holds widgets."""

import collections
import logging
from typing import Tuple, List

import wx

# pylint: disable=unused-import
from aio_wx_widgets import type_annotations as T
from aio_wx_widgets.binding import Binding

_LOGGER = logging.getLogger(__name__)


def _make_window(item: wx.Window, margins: List[Tuple[int, int]]):
    val = margins[0][1]
    for margin in margins[1:]:
        val = val | margin[1]

    new_sizer = wx.BoxSizer()
    margin_value = margins[0][0]
    new_sizer.Add(item, 1, val, margin_value)
    return new_sizer


def _margin_wrapper(item, margins: List[Tuple[int, int]]) -> wx.Window:
    if len(margins) == 0:
        return item

    first = margins.pop(0)

    values = [first]
    for idx, _ in enumerate(margins):
        if margins[idx][0] == first[0]:
            values.append(margins.pop(idx))

    item = _make_window(item, values)
    return _margin_wrapper(item, margins)


def _add(item, parent, sizer, weight, layout, margin, default_margin, create) -> object:
    if create:
        item = item(parent)

    if margin is None:
        margin = default_margin
    elif isinstance(margin, collections.Sequence):
        margins = [
            (margin[0], wx.LEFT),
            (margin[1], wx.RIGHT),
            (margin[2], wx.TOP),
            (margin[3], wx.BOTTOM),
        ]
        item = _margin_wrapper(item, margins)
        margin = 0

    sizer.Add(item, weight, layout, margin)

    return item


class PanelMixin:
    """Mixin providing extra functionality."""

    def __init__(self, parent):
        super().__init__(parent)
        self.Bind(wx.EVT_WINDOW_DESTROY, self._on_close)

    def _on_close(self, evt):
        _LOGGER.debug("Window destroyed.")
        self.controller.deactivate()
        evt.Skip()

    @property
    def controller(self) -> "T.BaseController":
        """Return the controller for this panel."""
        raise NotImplementedError()

    def bind(self, prop: str):
        """Bind a property to a bindable control.

        Args:
            prop: the attribute/property to bind.
        """
        return Binding(self.controller, prop)

    def add(self, item, weight=0, layout=wx.EXPAND | wx.ALL, margin=None, create=True):
        """Add an item to this panel

        Args:
            item: the item to be added.
            weight: The relative weight to other items in this container and the size
                it should take
            layout: The layout
            margin: None to use default. An int to use one margin for all sides.
                A tuple (left,right,top,bottom) for side specific margins.
            create: A ready made component can be added to.
        """
        return _add(
            item,
            self,
            self._sizer,
            weight,
            layout,
            margin,
            SimplePanel.default_sizer_margin,
            create,
        )

    def populate(self):
        """Add and configure widgets here."""


class SimplePanel(PanelMixin, wx.Panel):
    """A simple panel."""

    default_sizer_margin = 5

    @property
    def controller(self) -> "T.BaseController":
        raise NotImplementedError()

    def __init__(self, parent):
        """Init."""

        super().__init__(parent)

        self._sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self._sizer)
