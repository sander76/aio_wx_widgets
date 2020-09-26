from __future__ import annotations

import logging
from random import randint

from aio_wx_widgets.controller import BaseController

_LOGGER = logging.getLogger(__name__)


class ControllerThree(BaseController):
    def __init__(self, model):
        self.value_1: int = 0
        self.a_string_value = "A certain string"
        super().__init__(model)

    async def set_value(self):
        val = randint(1, 100)
        _LOGGER.debug("Setting bound property to %s", val)
        self.value_1 = val
