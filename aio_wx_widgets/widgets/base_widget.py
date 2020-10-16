from __future__ import annotations

import logging
from typing import Optional

from aio_wx_widgets import type_annotations as T
from aio_wx_widgets.core.binding import Binding, OneWayBindable

_LOGGER = logging.getLogger(__name__)


class BaseWidget:
    def __init__(self, ui_item: T.T_var, enabled: Optional[bool, Binding] = True):
        self._enabled = enabled
        self.ui_item = ui_item
        self._value_binding = None

        self._enabled_binding = None
        if isinstance(self._enabled, Binding):
            self._enabled_binding = OneWayBindable(
                self._enabled, self._set_enabled_value
            )

    def _set_enabled_value(self, enabled):
        if enabled:
            self.ui_item.Enable()
        else:
            self.ui_item.Disable()

    def _make_bindings(self):
        if self._value_binding:
            self._value_binding.make_binding()
        if self._enabled_binding:
            self._enabled_binding.make_binding()
