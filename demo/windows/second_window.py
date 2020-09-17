import logging

from aio_wx_widgets.frame import DefaultFrame
from demo.model.demo_model import DemoModel
from demo.controller import demo_controller_one
from demo.views.demo_views import DemoViewOne

_LOGGER = logging.getLogger(__name__)


class SecondWindow(DefaultFrame):
    def __init__(self):
        super().__init__("second window")

        model = DemoModel()
        controller = demo_controller_one.DemoController(model)
        view = DemoViewOne(self, controller)
        view.populate()
