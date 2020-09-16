import logging

from aio_wx_widgets.binding import Binding
from aio_wx_widgets.panels.panel import SimplePanel
from aio_wx_widgets.widgets.button import async_button
from aio_wx_widgets.widgets.grid import Grid, VERTICAL
from aio_wx_widgets.widgets.group import Group
from aio_wx_widgets.widgets.text import Text
from aio_wx_widgets.widgets.text_entry import IntEntry, Entry

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from demo.controller.demo_controller import DemoController


_LOGGER = logging.getLogger(__name__)


class DemoView(SimplePanel):
    def __init__(self, parent, controller: "DemoController"):
        self._controller = controller
        super().__init__(parent)

    @property
    def controller(self) -> "DemoController":
        return self._controller

    def populate(self):
        """Populate this view."""
        with self.add(Group("Number text entries.")) as group:
            with group.add(Grid()) as grd:
                grd.add(IntEntry(binding=self.bind("value_1")), weight=6, margin=3)
                grd.add(IntEntry(binding=self.bind("value_1")), weight=4, margin=3)
                grd.add(IntEntry(binding=self.bind("value_1")), weight=4, margin=3)

        with self.add(Group("Any text entry.")) as group:
            group.add(Entry(binding=Binding(self._controller, "a_string_value")))
            group.add(Entry(binding=Binding(self._controller, "a_string_value")))
        self.add(Text("This is a text."))
        with self.add(Grid()) as grd:

            grd.add(async_button("button one", self._set_value), weight=6)
            grd.add(async_button("button two,self", self._set_value), weight=6)

        with self.add(Group("Nesting of grids")) as grp:
            with grp.add(Grid()) as grd:
                grd.add(Text(text="A text"), weight=6, margin=2)
                with grd.add(Grid(VERTICAL), weight=6) as vert_grid:
                    vert_grid.add(async_button("Set number entries.", self._set_value))
                    vert_grid.add(
                        Text(text="This is some text"), margin=(10, 10, 30, 5)
                    )
                    vert_grid.add(async_button("button two,self", self._set_value))

        self.add(async_button("open other window", self._on_close))

    async def _on_close(self, evt):
        await self._controller.open_other_window()

    async def _on_open(self, evt):
        await self._controller.open_other_window()

    async def _set_value(self, evt):
        await self._controller.set_value()


class DemoViewOne(SimplePanel):
    def __init__(self, parent, controller: "DemoController"):
        self._controller = controller
        super().__init__(parent)

    def populate(self):
        self.add(
            IntEntry(binding=Binding(self._controller, "value_1")),
            margin=(10, 10, 5, 20),
        )
        self.add(IntEntry(binding=Binding(self._controller, "value_1")))
        self.add(async_button("test button", self._press), margin=(10, 10, 5, 20))

    async def _press(self, *args, **kwargs):
        pass
