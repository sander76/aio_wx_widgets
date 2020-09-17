"""All type annotations go here."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aio_wx_widgets.controller import BaseController
    from asyncio import AbstractEventLoop

    assert BaseController
    assert AbstractEventLoop
