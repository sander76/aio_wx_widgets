import logging

from aio_wx_widgets.panels.panel import SimplePanel
from aio_wx_widgets.widgets.button import async_button
from aio_wx_widgets.widgets.text_entry import IntEntry

_LOGGER = logging.getLogger(__name__)


class DemoView(SimplePanel):
    def __init__(self, parent):
        self._controller = None
        super().__init__(parent)

    def populate(self):
        self.add(IntEntry(binding=(self._controller, "value_1")))
        self.add(IntEntry(binding=(self._controller, "value_1")))
        self.add(async_button("open other window",self._on_open))
        self.add(async_button("set value",self._set_value))

    async def _on_open(self,evt):
        await self._controller.open_other_window()

    async def _set_value(self, evt):
        await self._controller.set_value()


class DemoViewOne(SimplePanel):
    def __init__(self, parent):
        self._controller = None
        super().__init__(parent)

    def populate(self):
        self.add(IntEntry(binding=(self._controller, "value_1")))
        self.add(IntEntry(binding=(self._controller, "value_1")))
