import logging
import wx
from wxasync import AsyncBind

from aio_wx_widgets.colors import GREEN
import os

_LOGGER = logging.getLogger(__name__)

debug = os.getenv("DEV_DEBUG")


def async_button(label, callback, parent=None):
    """Button with async binding."""
    btn = wx.Button()

    if debug:
        btn.SetBackgroundColour(GREEN)

    def _create(parent):
        btn.Create(parent, -1, label=str(label))
        AsyncBind(wx.EVT_BUTTON, callback, btn)
        return btn

    if parent is None:
        return _create
    return _create(parent)
