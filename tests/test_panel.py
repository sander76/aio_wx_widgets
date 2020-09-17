import logging

import wx

from aio_wx_widgets.panels.panel import _margin_wrapper

_LOGGER = logging.getLogger(__name__)


class MockWxWindow:
    def __init__(self, parent, *args, **kwargs):
        """Dummy init"""
        self.parent = parent
        self.sizer = None

    def SetSizer(self, sizer):
        self.sizer = sizer


class MockWxSizer:
    def __init__(self, *args, **kwargs):
        """mock init"""
        self.item = None
        self.margin = None
        self.layout = None
        self.stretch = None

    def Add(self, item, weight, layout, margin):
        self.item = item
        self.margin = margin
        self.layout = layout
        self.stretch = weight


def test_margin_wrapper(mocker):
    """Smoke test.

    If it runs. It is a success.
    """
    mocker.patch.object(wx, "Window", MockWxWindow)
    mocker.patch.object(wx, "BoxSizer", MockWxSizer)

    margins = [(10, wx.LEFT), (10, wx.RIGHT), (1, wx.TOP), (2, wx.BOTTOM)]

    item = MockWxWindow(None)
    window = _margin_wrapper(item, margins)
    print(window)
