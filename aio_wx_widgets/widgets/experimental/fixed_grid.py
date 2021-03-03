from __future__ import annotations

import logging

import wx

from aio_wx_widgets.core.base_widget import CallableItem

_LOGGER = logging.getLogger(__name__)


class FixedGrid(CallableItem):
    def __init__(self):
        self._sizer_ = wx.GridSizer(1, 0, (0, 0))
        self._parent = None

    @property
    def ui_item(self):
        return self._sizer_

    @property
    def _sizer(self):
        return self._sizer_

    def init(self, parent):
        self._parent = parent

    def __call__(self, parent):
        self.init(parent)
        return self

    def __enter__(self) -> FixedGrid:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager."""

    def add(self, item, create=True):
        used_cols = self._sizer_.GetEffectiveColsCount()
        _LOGGER.debug("Used cols %s", used_cols)
        total_cols = self._sizer_.GetCols()

        if create:
            assert isinstance(item, CallableItem)
            item.init(self._parent)

        if total_cols == used_cols:
            self._sizer_.SetCols(used_cols + 1)

        self._sizer_.Add(item.ui_item, 1, wx.EXPAND)
        return item


class DynamicGrid(CallableItem):
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

    def init(self, parent):
        self._parent = parent

    def __call__(self, parent):
        self.init(parent)
        return self

    def __enter__(self) -> DynamicGrid:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager."""

    def add(self, item, col, span=1, create=True):
        # used_cols = self._sizer_.GetEffectiveColsCount()
        # _LOGGER.debug("Used cols %s", used_cols)
        # total_cols = self._sizer_.GetCols()

        if create:
            assert isinstance(item, CallableItem)
            item.init(self._parent)

        # if total_cols == used_cols:
        #     self._sizer_.SetCols(used_cols + 1)
        self._sizer_.Add(item.ui_item, (0, col), (1, span), flag=wx.EXPAND)

        for idx in range(self._sizer_.Cols):
            if not self._sizer_.IsColGrowable(idx):
                self._sizer_.AddGrowableCol(idx)
        return item
