import asyncio
import logging
import os
from wxasync import WxAsyncApp

from aio_wx_widgets.controller import BaseController
from aio_wx_widgets.frame import DefaultFrame
from aio_wx_widgets.panels.panel import SimplePanel
from aio_wx_widgets.widgets.text_entry import IntEntry

_LOGGER = logging.getLogger(__name__)


class DemoModel:
    pass


class DemoController(BaseController):
    def __init__(self, view, model):
        self.value_1: int = 0
        super().__init__(view, model)


class DemoView(SimplePanel):
    def __init__(self, parent):
        self._controller = None
        super().__init__(parent)

    def populate(self):
        self.add(IntEntry(binding=(self._controller, "value_1")))
        self.add(IntEntry(binding=(self._controller, "value_1")))


class MainWindow(DefaultFrame):
    def __init__(self):
        super().__init__("Main window")

        model = DemoModel()
        view = DemoView(self)
        controller = DemoController(view, model)
        self.add(controller.view, create=False)


if __name__ == "__main__":
    os.environ["DEBUGGING"] = "1"
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    app = WxAsyncApp()
    main_window = MainWindow()
    main_window.Show()
    app.SetTopWindow(main_window)
    loop.run_until_complete(app.MainLoop())

# mypy .\start.py --check-untyped-defs
