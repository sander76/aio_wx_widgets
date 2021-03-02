"""Grid layout item."""

# pylint: disable=duplicate-code

from __future__ import annotations

import logging

import wx

from aio_wx_widgets.core.base_widget import CallableItem
from aio_wx_widgets.core.sizers import SizerMixin

_LOGGER = logging.getLogger(__name__)

__all__ = ["Grid", "VERTICAL", "HORIZONTAL"]

VERTICAL = wx.VERTICAL
HORIZONTAL = wx.HORIZONTAL


class Grid(SizerMixin, CallableItem):
    """A grid component.

    Basically a boxsizer with some defaults.
    """

    default_sizer_margin = 0

    HOR = HORIZONTAL
    VER = VERTICAL

    def __init__(self, orientation=HORIZONTAL):
        """Init."""
        super().__init__()
        self._sizer_ = wx.BoxSizer(orient=orientation)
        self._parent = None

    @property
    def ui_item(self):
        """Return UI item."""
        return self._sizer_

    @property
    def _sizer(self):
        return self._sizer_

    def init(self, parent):
        self._parent = parent

    def __call__(self, parent):
        # setting a specific parent.
        self.init(parent)
        return self

    def __enter__(self):
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""


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
