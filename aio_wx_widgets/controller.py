"""MVC controller."""

import logging

from aio_wx_widgets.binding import WATCHERS

_LOGGER = logging.getLogger(__name__)


class BaseController:
    """Base implementation of a controller."""

    def __init__(self, model: object):
        """Init.

        Args:
            view: The view part.
            model: The model.
        """

        self.model = model

    def __setattr__(self, item, value):
        print(f"Setting item {item} to value {value}")
        self.__dict__[item] = value
        if WATCHERS not in self.__dict__:
            return
        if item not in self.__dict__[WATCHERS]:
            return

        watchers = self.__dict__[WATCHERS][item]
        for watcher in watchers:
            watcher(value)
