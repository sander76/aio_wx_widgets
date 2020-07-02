import logging
from typing import Tuple, Any

from aio_wx_widgets.controller import BaseController
from demo.view_controllers_factory.demo_controller import DemoController
from demo.view_controllers_factory.demo_view import DemoView, DemoViewOne

_LOGGER = logging.getLogger(__name__)


def get_demo_controller_view(parent, model) -> Tuple[Any, BaseController]:
    view = DemoView(parent)
    controller = DemoController(view, model)
    view._controller = controller
    view.populate()
    return view, controller

def get_demo_controller_one(parent,model) ->Tuple[Any,BaseController]:
    view = DemoViewOne(parent)
    controller = DemoController(view, model)
    view._controller = controller
    view.populate()
    return view, controller