import logging

import wx
from demo.controller.image_view_controller import ImageViewController
from demo.model.demo_model import DemoModel
from demo.views.image_view import ImageView

from aio_wx_widgets.frame import DefaultFrame

_LOGGER = logging.getLogger(__name__)


class ImageViewWindow(DefaultFrame):
    def __init__(self):
        super().__init__("Text wrapping window")

        model = DemoModel()
        controller = ImageViewController(model)
        self.view = ImageView(self, controller)
        self.view.populate()
        self.view.ui_item.PostSizeEvent()

        self.Bind(wx.EVT_MAXIMIZE, self._on_max)

    def _on_max(self, evt):
        evt.Skip()
        self.view.ui_item.PostSizeEvent()
