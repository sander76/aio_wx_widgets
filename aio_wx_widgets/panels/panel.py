"""Panel. Sits in a frame. Holds widgets."""

import logging

import wx

# pylint: disable=unused-import
from aio_wx_widgets import type_annotations as T
from aio_wx_widgets.sizers import PanelMixin

_LOGGER = logging.getLogger(__name__)


class SimplePanel(PanelMixin, wx.Panel):
    """A simple panel."""

    def __init__(self, parent, **kwargs):
        """Init."""

        self._sizer = wx.BoxSizer(wx.VERTICAL)

        kwargs["parent"] = parent
        kwargs["sizer"] = self._sizer
        super().__init__(**kwargs)
        # super(PanelMixin,self).parent = parent
        self.SetSizer(self._sizer)

    @property
    def controller(self) -> "T.BaseController":
        raise NotImplementedError()
