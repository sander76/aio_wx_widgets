import logging
from typing import Optional, Callable, Union

import wx

from aio_wx_widgets.core.binding import Bindable, Binding
from aio_wx_widgets.widgets.base_widget import BaseWidget

_LOGGER = logging.getLogger(__name__)

__all__ = ["CheckBox"]


class CheckBox(BaseWidget):
    def __init__(
        self,
        label: str,
        binding: Binding,
        change_callback: Optional[Callable[[bool], None]] = None,
        enabled: Union[bool, Binding] = True,
        min_width=-1,
    ):
        """Init.

        Args:
            label: Checkbox label
            binding: property binding.
            change_callback: called when checkbox value changes.
        """
        super().__init__(wx.CheckBox(), min_width=min_width, enabled=enabled)
        self._label = str(label)
        self._change_callback = change_callback

        self._value_binding = Bindable(binding, self._get_ui_value, self._set_ui_value)

    def _set_ui_value(self, value):
        val = bool(value)
        _LOGGER.debug("Setting value to %s, %s", val, id(self))
        self.ui_item.SetValue(val)

        # setting this value manually as the SetValue command does -in this case-
        # not trigger the _on_ui_change callback.
        self._value_binding._fire_update_event = True

    def _get_ui_value(self, force: bool) -> bool:
        val = self.ui_item.GetValue()
        return val

    def _on_ui_change(self, *args, **kwargs):
        self._value_binding.on_ui_change(*args, **kwargs)

        if self._change_callback:
            self._change_callback(self._get_ui_value(True))

    def __call__(self, parent):
        self.ui_item.Create(parent, label=self._label)
        self.ui_item.Bind(wx.EVT_CHECKBOX, self._on_ui_change)

        # self._make_bindings()
        self._init()

        return self
