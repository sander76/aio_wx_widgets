"""Sizer and Layout tooling."""
from __future__ import annotations

import collections
import logging
from typing import List, Tuple, Optional, Union

import wx

from aio_wx_widgets import type_annotations as T  # noqa
from aio_wx_widgets.core.binding import Binding
from aio_wx_widgets.core.data_types import HorAlign, VerAlign

_LOGGER = logging.getLogger(__name__)

# T_var = TypeVar("T_var")


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


def _align_item(
    item: Union[wx.Window, wx.BoxSizer],
    current_sizer_orientation,
    hor_align: Optional["HorAlign"],
    ver_align: Optional[VerAlign],
    current_layout: int,
) -> Tuple[Union[wx.Window, wx.BoxSizer], int]:

    if current_sizer_orientation == wx.VERTICAL:
        _LOGGER.debug("Current sizer is vertical")
        if hor_align:
            _LOGGER.debug("Item has hor alignment set.")
            current_layout = current_layout | hor_align.value
            return _align_item(
                item, current_sizer_orientation, None, ver_align, current_layout
            )
    if current_sizer_orientation == wx.HORIZONTAL:
        _LOGGER.debug("Current sizer is horizontal.")
        if ver_align:
            _LOGGER.debug("Item has ver alignment set.")
            current_layout = current_layout | ver_align.value
            return _align_item(
                item, current_sizer_orientation, hor_align, None, current_layout
            )
    if hor_align:
        _LOGGER.debug(
            "Setting a horizontal alignment but current orientation is %s",
            current_sizer_orientation,
        )
        sizer = wx.BoxSizer(orient=wx.VERTICAL)
        sizer.Add(item, 0, hor_align.value, 0)
        return _align_item(sizer, wx.VERTICAL, None, ver_align, current_layout)

    if ver_align:
        sizer = wx.BoxSizer()
        sizer.Add(item, 0, ver_align.value, 0)
        return _align_item(sizer, wx.HORIZONTAL, hor_align, None, current_layout)
    return item, current_layout


def _add(
    item: T.Widget,
    parent,
    sizer,
    weight,
    margin,
    default_margin,
    create,
    hor_align: Optional[HorAlign],
    ver_align: Optional[VerAlign],
) -> T.Widget:
    if create:
        # this is an item which is part of the aio_wx_widgets family.
        # It is assumed it has the ui_item property.
        item = item(parent)
        ui_item = item.ui_item
    else:
        # this is assumed to be a "normal" wx-widgets item.
        ui_item = item
    if margin is None:
        margin = default_margin
    elif isinstance(margin, collections.Sequence):
        margins = [
            (margin[0], wx.LEFT),
            (margin[1], wx.RIGHT),
            (margin[2], wx.TOP),
            (margin[3], wx.BOTTOM),
        ]
        ui_item = _margin_wrapper(ui_item, margins)
        margin = 0

    layout = wx.ALL

    _LOGGER.debug(
        ">> Aligning %s, ver_align(%s), hor_align(%s)", type(item), ver_align, hor_align
    )
    if hor_align is None and ver_align is None:

        layout = layout | wx.EXPAND
    else:
        ui_item, layout = _align_item(
            ui_item, sizer.Orientation, hor_align, ver_align, layout
        )

    sizer.Add(ui_item, weight, layout, margin)

    return item


class SizerMixin:
    """Mixin providing sizer functionality"""

    default_sizer_margin = 5

    def add(
        self,
        item: T.Widget,
        weight=0,
        margin=(5, 5, 1, 1),  # left,right,top,bottom
        create=True,
        hor_align: Optional[HorAlign] = None,
        ver_align: Optional[VerAlign] = None,
    ) -> T.Widget:
        """Add an item to this panel

        Args:
            item: the item to be added.
            weight: The relative weight to other items in this container and the size
                it should take
            margin: An int to use one margin for all sides.
                A tuple (left,right,top,bottom) for side specific margins.
            create: A ready made component can be added to.
            hor_align: Horizontal alignment.
            ver_align: Vertical alignment.
        """
        try:
            parent = self._parent  # type: ignore
            if parent is None:
                raise AttributeError("parent cannot be none.")
        except AttributeError:
            parent = self.ui_item  # type: ignore

        return _add(
            item,
            parent,
            self._sizer,  # type: ignore
            weight,
            margin,
            SizerMixin.default_sizer_margin,
            create,
            hor_align=hor_align,
            ver_align=ver_align,
        )

    def add_space(self, proportion=1):
        """Add a stretching spacer."""
        self._sizer.AddStretchSpacer(prop=proportion)


class PanelMixin:
    """Mixin providing extra functionality."""

    def __init__(self):
        self.ui_item.Bind(wx.EVT_WINDOW_DESTROY, self._on_close)
        super().__init__()

    def _on_close(self, evt):
        _LOGGER.debug("Window destroyed.")
        self.controller.deactivate()
        evt.Skip()

    @property
    def controller(self) -> T.BaseController:
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
