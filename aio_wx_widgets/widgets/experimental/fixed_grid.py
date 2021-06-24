"""A fixed grid.

when resizing windows this layout seems to be most reliable.
"""

from __future__ import annotations

import logging

import wx

from aio_wx_widgets.core.base_widget import CallableItem
from aio_wx_widgets.core.sizers import ItemType

_LOGGER = logging.getLogger(__name__)


class FixedGrid(CallableItem):
    """A fixed grid implementation.

    When resizing windows this grid behaves best.
    """

    def __init__(self):
        self._sizer_ = wx.GridSizer(1, 0, (0, 0))
        self._parent = None

    @property
    def ui_item(self):
        return self._sizer_

    @property
    def _sizer(self) -> wx.GridSizer:
        return self._sizer_

    def init(self, parent: wx.Window):
        self._parent = parent

    def __call__(self, parent: wx.Window):
        self.init(parent)
        return self

    def __enter__(self) -> FixedGrid:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # type:ignore
        """Exit the context manager."""

    def _check_columns(self):
        used_cols: int = self._sizer_.GetEffectiveColsCount()
        _LOGGER.debug("Used cols %s", used_cols)
        total_cols: int = self._sizer_.GetCols()
        if total_cols == used_cols:
            self._sizer_.SetCols(used_cols + 1)

    def add(self, item: ItemType, create: bool = True) -> ItemType:
        """Add an item to this grid."""
        self._check_columns()
        if create:
            assert isinstance(item, CallableItem)
            item.init(self._parent)

        self._sizer_.Add(item.ui_item, 1, wx.EXPAND)  # type:ignore
        return item

    def add_spacer(self):
        """Add an empty space to a column."""
        self._check_columns()
        self._sizer_.Add(wx.Panel(self._parent), 1, flag=wx.EXPAND)  # type: ignore


class DynamicGrid(CallableItem):
    """A dynamic grid. Allows for column spanning etc."""

    def __init__(self):
        self._sizer_ = wx.GridBagSizer()
        self._sizer_.SetFlexibleDirection(wx.VERTICAL)
        self._sizer_.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_ALL)
        self._parent = None

    @property
    def ui_item(self):
        return self._sizer_

    @property
    def _sizer(self):
        return self._sizer_

    def init(self, parent: wx.Window):
        self._parent = parent
        # self._parent.Bind(wx.EVT_SIZE,self._on_size)

    def _on_size(self, evt: wx.SizeEvent):
        evt.Skip()

        _LOGGER.debug(
            "Laying out dynamic grid. %s, sizer width %s, parent sizxe",
            evt.Size,
            self._parent.Size,
        )
        # wx.CallAfter(self.ui_item.PostSizeEvent())

    def __call__(self, parent: wx.Window):
        self.init(parent)
        return self

    def __enter__(self) -> DynamicGrid:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # type: ignore
        """Exit the context manager."""

    def add(
        self, item: ItemType, col: int, span: int = 1, create: bool = True
    ) -> ItemType:
        """Add an item to this grid."""

        if create:
            assert isinstance(item, CallableItem)
            item.init(self._parent)

        self._sizer_.Add(item.ui_item, (0, col), (1, span), flag=wx.EXPAND)  # type: ignore
        self._set_col_sizes_equal()
        return item

    def _set_col_sizes_equal(self):
        for idx in range(self._sizer_.Cols):
            if not self._sizer_.IsColGrowable(idx):  # type: ignore
                self._sizer_.AddGrowableCol(idx)  # type: ignore

    def add_spacer(self, col, span=1):
        """Add an empty space to a column and/or span."""
        self._sizer_.Add(wx.Panel(self._parent), (0, col), (1, span), flag=wx.EXPAND)
        self._set_col_sizes_equal()
