import logging
from pathlib import Path

from demo.controller.image_view_controller import ImageViewController

from aio_wx_widgets.containers import Grid
from aio_wx_widgets.panels.panel import SimplePanel
from aio_wx_widgets.widgets import Text
from aio_wx_widgets.widgets.experimental.fixed_grid import FixedGrid
from aio_wx_widgets.widgets.image import Image

_LOGGER = logging.getLogger(__name__)

IMAGE_FOLDER = (Path(__file__).parent) / "image"


class ImageView(SimplePanel[ImageViewController]):
    """A text wrapping view test."""

    def populate(self):
        # self.add(Image(IMAGE_FOLDER / "phoenix_main.png"), weight=1)
        with self.add(FixedGrid()) as grd:
            # grd.add_space()
            grd.add(Text("this is text"))
            grd.add(Image(IMAGE_FOLDER / "phoenix_main.png"))

        with self.add(FixedGrid(), weight=1) as grd:
            with grd.add(Grid(orientation=Grid.VER)) as column1:
                column1.add_space(1)

            with grd.add(Grid(orientation=Grid.VER)) as column2:
                column2.add(Image(IMAGE_FOLDER / "phoenix_main.png"), weight=1)
