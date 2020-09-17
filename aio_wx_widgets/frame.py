"""WX ui frames. A windows that holds a panel."""

import logging
from pathlib import Path
from typing import Optional

import wx

_LOGGER = logging.getLogger(__name__)


def _get_app_icon_32(img_path: Path):
    app_icon_32 = wx.Icon()
    app_icon_32.CopyFromBitmap(wx.Bitmap(str(img_path), wx.BITMAP_TYPE_PNG))
    return app_icon_32


class DefaultFrame(wx.Frame):
    """A default frame for app windows.

    Always add a panel to this frame first.
    """

    def __init__(
        self,
        title,
        parent=None,
        size: wx.Size = None,
        style=None,
        icon_img: Optional[Path] = None,
    ):
        """Init.

        Args:
            title:
            parent:
            size:
            style:
        """
        kwargs = {}
        if style is not None:
            kwargs["style"] = style

        if size is None:
            size = wx.Size(800, 600)

        kwargs["size"] = size
        kwargs["title"] = title

        wx.Frame.__init__(self, parent, **kwargs)
        if icon_img:
            self.SetIcon(_get_app_icon_32(icon_img))

        self.Bind(wx.EVT_CLOSE, self._on_close)

    def _on_close(self, evt):
        _LOGGER.debug("Frame is closed.")
        evt.Skip()
