import logging
from typing import TYPE_CHECKING

from aio_wx_widgets.binding import Binding
from aio_wx_widgets.panels.panel import SimplePanel
from aio_wx_widgets.sizers import AlignHorizontal
from aio_wx_widgets.widgets.button import AioButton
from aio_wx_widgets.widgets.grid import Grid, VERTICAL
from aio_wx_widgets.widgets.group import Group
from aio_wx_widgets.widgets.text import Text
from aio_wx_widgets.widgets.text_entry import IntEntry, Entry

if TYPE_CHECKING:
    from demo.controller.demo_controller import DemoController
    from demo.controller import demo_controller_one

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

        # Use a context manager for container types like a group or grid.
        # A group is a container with a label and a sizer inside. Inside
        # this sizer widgets, or other containers can be placed.
        with self.add(Group("A labelled container.")) as group:
            group.add(Text(text="A horizontal grid."))

            with group.add(Grid()) as grd:
                # the binding binds to an attribute defined in the controller
                # the weight determines how much space a specific item should consume
                # with respect to the other members of the container.
                grd.add(IntEntry(binding=self.bind("value_1")), weight=6, margin=3)
                grd.add(IntEntry(binding=self.bind("value_1")), weight=4, margin=3)
                grd.add(IntEntry(binding=self.bind("value_1")), weight=4, margin=3)

        with self.add(Group("Any text entry.")) as group:
            group.add(Entry(binding=Binding(self._controller, "a_string_value")))
            group.add(Entry(binding=Binding(self._controller, "a_string_value")))

        with self.add(Grid()) as grd:
            grd.add(AioButton("button one", self._set_value), weight=6)
            grd.add(AioButton("button two,self", self._set_value), weight=6)

        with self.add(Group("Nesting of grids")) as grp:
            with grp.add(Grid()) as grd:
                grd.add(
                    Text(text="Right aligned text"),
                    weight=3,
                    margin=5,
                    align_horizontal=AlignHorizontal.right,
                )
                with grd.add(Grid(VERTICAL), weight=6, margin=0) as vert_grid:
                    vert_grid.add(
                        AioButton("Left aligned button", self._set_value),
                        align_horizontal=AlignHorizontal.left,
                        margin=4,
                    )
                    vert_grid.add(AioButton("Set number entries.", self._set_value))
                    vert_grid.add(
                        Text(text="Center aligned text with a large margin."),
                        margin=(10, 10, 30, 5),
                        align_horizontal=AlignHorizontal.center,
                    )
                    vert_grid.add(
                        AioButton("right aligned button.", self._set_value),
                        weight=2,
                        align_horizontal=AlignHorizontal.right,
                    )

        self.add(AioButton("open other window", self._on_open_second_window))

    async def _on_open_second_window(self, evt):
        await self._controller.open_other_window()

    async def _on_open(self, evt):
        await self._controller.open_other_window()

    async def _set_value(self, evt):
        await self._controller.set_value()


class DemoViewOne(SimplePanel):
    """Second view."""

    def __init__(self, parent, controller: "demo_controller_one.DemoController"):
        self._controller = controller
        super().__init__(parent)
        self._text = Text("This is text that changes as a result of an event happening")
        self._controller.add_to_log.subscribe(self._add_to_log)

    @property
    def controller(self) -> "demo_controller_one.DemoController":
        return self._controller

    def populate(self):
        self.add(
            IntEntry(binding=Binding(self._controller, "value_1")),
            margin=(10, 10, 5, 20),
        )
        self.add(IntEntry(binding=Binding(self._controller, "value_1")))
        self.add(
            AioButton("test button with normal function as callback", self._press),
            margin=(10, 10, 5, 20),
        )
        self.add(self._text)

    def _press(self, evt):
        self._add_to_log("button pressed.")

    def _add_to_log(self, item: str):
        self._text.set_text(item)
