import logging
import wx
import asyncio
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from aiosubpub import Channel

_LOGGER = logging.getLogger(__name__)


class BaseController:
    """Base implementation of a controller."""

    def __init__(self, view, model: Any):
        """Init.

        Args:
            view: The view part.
            model: The model.
        """
        self.view = view
        self.view._controller = self
        self.view.populate()
        self.model = model

        self.view.Bind(wx.EVT_WINDOW_DESTROY, self._on_close)
        self.view.Bind(wx.EVT_CLOSE, self._on_close)

        self._channels = []
        # self._loop = asyncio.get_running_loop()

    def subscribe(self, channel: "Channel", callback):
        """Subscribe to a listener.

        On exit these listeners will be deleted.
        """

        subscription = channel.subscribe(callback)
        self._channels.append(subscription)
        return subscription

    def _on_close(self, event):
        _LOGGER.debug("cancelling tasks in _channels.")
        for task in self._channels:

            task.cancel()
        self._channels = []

        event.Skip()
