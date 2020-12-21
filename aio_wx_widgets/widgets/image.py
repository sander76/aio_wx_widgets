"""Image widget"""

import asyncio
import logging
from pathlib import Path

import wx

from aio_wx_widgets.core.base_widget import BaseWidget

_LOGGER = logging.getLogger(__name__)


def _get_ratio(image: wx.Image):
    size = image.GetSize()
    width_height = size[0] / size[1]
    return width_height


X_SIZE_CORRECTION = 2
REFRESH_DELAY = 0.1
WAKEUP_CHECK = 0.02  # this value should always be smaller than the REFRESH_DELAY


class Image(BaseWidget):
    """Autoscaling image widget."""

    def __init__(self, image: Path):
        super().__init__(wx.StaticBitmap(), min_width=-1, value_binding=None)
        self._image = wx.Image(str(image), wx.BITMAP_TYPE_PNG)
        self._image_ratio = _get_ratio(self._image)
        self._delayed_call_task = None
        self._delay = REFRESH_DELAY
        self._block_size_event = False  # If true it will skip the EVT_SIZE event.

    def init(self, parent):
        self.ui_item.Create(parent)
        self.ui_item.Bind(wx.EVT_SIZE, self._on_size)

    def __call__(self, parent):
        self.init(parent)
        return self

    async def _delayed_set_size(self):
        while self._delay > 0:

            await asyncio.sleep(WAKEUP_CHECK)
            self._delay -= WAKEUP_CHECK

        size = self.ui_item.ContainingSizer.Size
        self._block_size_event = True
        _LOGGER.debug("Setting final size to: %s", size)
        img_size = self._get_size(size)

        self._set_image(*img_size, dummy=False, redraw=True)
        self._delayed_call_task = None
        self._block_size_event = False

    def _on_size(self, evt):  # noqa
        if self._block_size_event:
            return
        size = self.ui_item.ContainingSizer.Size
        # _LOGGER.debug("container size %s", size)

        if size[0] <= 0 or size[1] <= 0:
            return
        if not self._delayed_call_task:
            try:
                _loop = asyncio.get_event_loop()
                self._delayed_call_task = _loop.create_task(self._delayed_set_size())
            except RuntimeError:
                _LOGGER.error("loop not started yet.")

        # reset the delayed refresh timer.
        self._delay = REFRESH_DELAY

        size = self._get_size(size)
        self._set_image(*size, dummy=True)

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
