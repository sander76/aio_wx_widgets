"""MVC controller."""
from __future__ import annotations

import asyncio
import logging
from asyncio import Task
from asyncio.futures import Future
from typing import Any, Awaitable, Callable, Generic, List, Optional, TypeVar

from aio_wx_widgets import type_annotations as T  # noqa
from aio_wx_widgets.core.binding import WATCHERS

_LOGGER = logging.getLogger(__name__)

#  pylint: disable=invalid-name
M = TypeVar("M")


class BaseController(Generic[M]):
    """Base implementation of a controller."""

    def __init__(self, model: M):
        """Init.

        Args:
            model: The model.
        """

        self._model = model
        self._tasks: List[Task[Any]] = []

    @property
    def model(self) -> M:
        """Return the model of this controller."""
        return self._model

    def __setattr__(self, item: str, value: object):
        super().__setattr__(item, value)
        if WATCHERS not in self.__dict__:
            return
        if item not in self.__dict__[WATCHERS]:
            return

        watchers = self.__dict__[WATCHERS][item]
        for watcher in watchers:
            watcher(value)

    @property
    def _loop(self) -> T.AbstractEventLoop:
        return asyncio.get_running_loop()

    def create_task(
        self,
        coro: Awaitable[object],
        callback: Optional[Callable[[Future[Any]], None]] = None,
    ) -> Task:
        """Create a task.

        When this step is deactivated, the task
        will be cancelled.
        """

        task: Task = self._loop.create_task(coro)
        if callback:
            task.add_done_callback(callback)
        self._tasks.append(task)
        return task

    def add_task(self, task):
        """Attach a task to this step.

        When step is deactivated, the
        task will be cancelled.
        """
        self._tasks.append(task)
        return task

    def deactivate(self):
        """Run on closing this step."""

        for task in self._tasks:
            task.cancel()
