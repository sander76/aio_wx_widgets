"""Text widgets."""

import logging
from typing import Optional

import wx

from aio_wx_widgets.binding import Bindable
from aio_wx_widgets.colors import GREEN
from aio_wx_widgets.const import is_debugging

_LOGGER = logging.getLogger(__name__)


class Text(Bindable):
    """Static text."""

    def __init__(
        self, text="", font_size=None, color: Optional[int] = None, binding=None
    ):
        """Init.

        Args:
            parent:
            text:
            font_size:
        """
        self._color = color
        self._text = text

        super().__init__(binding)

        self._font_size = None
        if font_size:
            self._font_size = wx.Font(wx.FontInfo(font_size))
        self.ui_item = wx.StaticText()

    def _set_ui_value(self, value):
        self.ui_item.SetLabelText(str(value))

    def _get_ui_value(self):
        """This is a one way binding. Not implementing this."""
        return None

    def __call__(self, parent):
        self.ui_item.Create(parent)
        if self._font_size:
            self.ui_item.SetFont(self._font_size)
        self.set_text(self._text, self._color)
        if is_debugging():
            self.ui_item.SetBackgroundColour(GREEN)
        self._make_binding()
        return self

    def set_text(self, text, color=None):
        """Set text."""
        self._text = str(text)
        self.ui_item.SetLabel(self._text)
        if color:
            self.ui_item.SetForegroundColour(color)
