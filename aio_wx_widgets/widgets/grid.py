"""Grid layout item."""

# pylint: disable=duplicate-code


import logging

import wx

from aio_wx_widgets.sizers import SizerMixin

_LOGGER = logging.getLogger(__name__)

VERTICAL = wx.VERTICAL
HORIZONTAL = wx.HORIZONTAL


class Grid(SizerMixin, wx.BoxSizer):
    """A grid component.

    Basically a boxsizer with some defaults.
    """

    default_sizer_margin = 0

    def __init__(self, orientation=HORIZONTAL, **kwargs):
        """Init."""
        kwargs["orient"] = orientation
        kwargs["sizer"] = self
        super().__init__(**kwargs)

    def __call__(self, parent):
        # the SizerMixin needs a parent. If below command is not run it will use
        # this Grid as a parent. Which is a BoxSizer, which cannot be a parent.
        super().set_parent(parent)
        return self

    # # pylint: disable=duplicate-code
    # def add(
    #     self,
    #     item,
    #     weight=0,
    #     layout=wx.EXPAND | wx.LEFT | wx.RIGHT,
    #     margin=None,
    #     create=True,
    # ):
    #     """Add a UI component to this UI container."""
    #     return _add(
    #         item,
    #         self.parent,
    #         self,
    #         weight,
    #         layout,
    #         margin,
    #         self.default_sizer_margin,
    #         create,
    #     )

    def __enter__(self):
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
