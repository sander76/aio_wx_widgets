import asyncio
import logging
from asyncio import CancelledError
from random import randint

from aiosubpub import Channel

from aio_wx_widgets.controller import BaseController

_LOGGER = logging.getLogger(__name__)


class DemoController(BaseController):
    def __init__(self, model):
        self.value_1: int = 0
        self.a_string_value = "A certain string"
        super().__init__(model)
        self.create_task(self.value_setter())
        self.add_to_log = Channel("Log messages")

    async def set_value(self):
        val = randint(1, 100)
        _LOGGER.debug("Setting bound property to %s", val)
        self.value_1 = val

    async def value_setter(self):
        try:
            while 1:
                val = str(randint(1, 100))
                _LOGGER.debug("Setting value to : %s", val)
                self.add_to_log.publish(val)
                await asyncio.sleep(2)
        except CancelledError:
            _LOGGER.debug("Stopping value setter task.")
