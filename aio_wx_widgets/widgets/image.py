"""Image widget"""

import logging
from pathlib import Path

import wx

from aio_wx_widgets.colors import RED
from aio_wx_widgets.const import is_debugging
from aio_wx_widgets.core.base_widget import BaseWidget

_LOGGER = logging.getLogger(__name__)


def _get_ratio(image: wx.Image):
    size = image.GetSize()
    width_height = size[0] / size[1]
    return width_height


class SizeableImage(wx.Panel):
    def __init__(self, *args, **kwargs):
        self._image_ratio = kwargs.pop("ratio")
        self._min_width = 100

        super().__init__(*args, **kwargs)
        if is_debugging():
            self.SetBackgroundColour(RED)

    def DoGetBestClientSize(self):
        container_size = self.ContainingSizer.Size
        _LOGGER.debug("containersize: %s", container_size)
        if container_size[0] < 20:
            min_x = self._min_width
        else:
            min_x = container_size[0] - 20

        optimal_size = (-1, min_x / self._image_ratio)
        _LOGGER.debug("called DoGetBestClientSize, returning %s", optimal_size)

        return optimal_size


class Image(BaseWidget):
    """Autoscaling image widget."""

    def __init__(self, image: Path):
        self._image = wx.Image(str(image), wx.BITMAP_TYPE_PNG)
        self._image_ratio = _get_ratio(self._image)
        super().__init__(
            SizeableImage(ratio=self._image_ratio), min_width=10, value_binding=None
        )

    def init(self, parent):
        self.ui_item.Create(parent)

        # self._set_image(10,10,dummy=False)
        parent.Bind(wx.EVT_SIZE, self._on_size)
        parent.Bind(wx.EVT_DISPLAY_CHANGED, self._on_max)
        self.ui_item.Layout()

    def _on_max(self, evt):
        _LOGGER.debug("Max event")

    def __call__(self, parent):
        self.init(parent)
        return self

    def _on_size(self, evt):  # noqa
        self.ui_item.InvalidateBestSize()
        evt.Skip()

    def _get_size(self, size):
        # _LOGGER.debug("Sizing image: %s", (parent_x, parent_y))

        image_x = size[0]
        image_y = image_x / self._image_ratio

        return image_x, image_y

    def _set_image(self, width, height, dummy: bool, redraw=False):
        """Set the image.

        Args:
            width: width of the image
            height: height of the image
            dummy: If true a dummy image will be used.
                While sizing a window this is used keep the layout of the screen intact
                (more specifically the image height) while reducing compute power
                by having to scale the original image.
            redraw: Redraw and re-layout the entire window.
        """
        if dummy:
            # _LOGGER.debug("Setting dummy image")
            bitmap = wx.Bitmap.FromRGBA(
                1,
                height,
                red=self.ui_item.BackgroundColour.red,
                green=self.ui_item.BackgroundColour.green,
                blue=self.ui_item.BackgroundColour.blue,
                alpha=self.ui_item.BackgroundColour.alpha,
            )
        else:
            _LOGGER.debug("Setting image size to : %s", (width, height))
            image = self._image.Scale(width, height, quality=wx.IMAGE_QUALITY_BICUBIC)
            bitmap = wx.Bitmap(image)

        self.ui_item.SetBitmap(bitmap)
        if redraw:

            # If omitted, the other items on screen look distorted.
            self.ui_item.Parent.Refresh()
            # seems to be required to correct the layout when restoring original
            # window size (Going from Max screen size to Original size)
            self.ui_item.Parent.Sizer.Layout()
