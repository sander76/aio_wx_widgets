"""Sizer and Layout tooling."""

import collections
import logging
from typing import List, Tuple

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


class SizerMixin:
    """Mixin providing sizer functionality"""

    default_sizer_margin = 5

    def __init__(self, sizer, **kwargs):
        self._sizer = sizer
        self._parent = None
        super().__init__(**kwargs)

    def set_parent(self, parent):
        """Explicitly set the parent.
        Use this when this Mixin is used inside a sizer (like boxsizer).

        If not set explicitly the sizer will be used as parent, which is not possible.
        """
        self._parent = parent

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
        parent = self._parent if self._parent is not None else self

        return _add(
            item,
            parent,
            self._sizer,
            weight,
            layout,
            margin,
            SizerMixin.default_sizer_margin,
            create,
        )


class PanelMixin(SizerMixin):
    """Mixin providing extra functionality."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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

    def populate(self):
        """Add and configure widgets here."""
