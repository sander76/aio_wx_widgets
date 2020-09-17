import logging

from aio_wx_widgets.frame import DefaultFrame
from demo.controller.demo_controller import DemoController
from demo.model.demo_model import DemoModel
from demo.views.demo_views import DemoView

_LOGGER = logging.getLogger(__name__)


class MainWindow(DefaultFrame):
    def __init__(self):
        super().__init__("Main window")

        model = DemoModel()
        controller = DemoController(model)
        view = DemoView(self, controller)
        view.populate()
