"""WX button."""

import logging
from asyncio import iscoroutinefunction
from typing import Callable, Any, Awaitable, Union

import wx
from wxasync import AsyncBind  # type: ignore

from aio_wx_widgets.core.binding import Binding
from aio_wx_widgets.widgets.base_widget import BaseWidget

_LOGGER = logging.getLogger(__name__)

__all__ = ["AioButton"]


class AioButton(BaseWidget):
    """Button widget.

    Args:
        label: button label.
        callback: a coroutine function or normal function. Called when pressed.
    """

    def __init__(
        self,
        label: str,
        callback: Union[Callable[[Any, Any], Awaitable], Callable[[Any, Any], None]],
        enabled: Union[bool, Binding] = True,
        min_width=-1,
    ):
        super().__init__(wx.Button(), min_width=min_width, enabled=enabled)
        self._label = label
        self._call_back = callback

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value: str):
        self._label = str(value)
        self.ui_item.SetLabelText(self._label)

    def __call__(self, parent):
        self.ui_item.Create(parent, label=self._label)
        if iscoroutinefunction(self._call_back):

            AsyncBind(wx.EVT_BUTTON, self._call_back, self.ui_item)
        else:
            self.ui_item.Bind(wx.EVT_BUTTON, self._call_back)

        # self._make_bindings()
        self._init()
        return self
