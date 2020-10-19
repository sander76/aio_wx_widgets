"""A dropdown selection widget."""

from __future__ import annotations
import logging
from typing import Callable, Optional, Sequence, Union

import wx
from aio_wx_widgets import type_annotations as T
from aio_wx_widgets.core.binding import Bindable, Binding
from aio_wx_widgets.widgets.base_widget import BaseWidget

_LOGGER = logging.getLogger(__name__)

__all__ = ["Select"]


class Select(BaseWidget):
    """Dropdown selection widget."""

    def __init__(
        self,
        choices: Sequence[T.Choice],
        on_select_callback: Optional[Callable[[T.Choice], None]] = None,
        binding: Optional[T.Binding] = None,
        min_width=300,
        enabled: Union[bool, Binding] = True,
    ):
        """
        Init.

        Args:
            choices: Used to populate the dropdown.
            on_select_callback: called when selection is made.
            binding:
            min_width: when alignment is set, this is the advised minimal width the
                the widget should take.
        """
        super().__init__(wx.Choice(), min_width, enabled)
        self.choices = choices
        self._on_select_callback = on_select_callback
        self._selected_item = None

        self.ui_item.Bind(wx.EVT_CHOICE, self._on_choice)
        self.ui_item.Bind(wx.EVT_MOUSEWHEEL, self._on_mouse_wheel)
        self._min_width = min_width
        self._value_binding = Bindable(binding, self._get_ui_value, self._set_ui_value)

    def _on_mouse_wheel(self, evt):
        """Capturing as I want to disable selection when scrolling"""

    # def init(self, parent):
    #     """Initialize the component."""

    def _set_ui_value(self, value: T.Choice):
        try:
            _idx = next(
                (i for i, val in enumerate(self.choices) if val.value == value.value)
            )
        except StopIteration:
            _LOGGER.error("Default product not available")
        else:
            self.ui_item.Select(_idx)

    def _on_choice(self, event):
        _idx = self.ui_item.GetSelection()
        _LOGGER.debug("Selected idx: %s", _idx)
        self._selected_item = self.choices[_idx]
        self._value_binding.on_ui_change()
        if self._on_select_callback:
            self._on_select_callback(self._selected_item)

    def _get_ui_value(self, force):
        return self._selected_item

    def __call__(self, parent):
        # self.init(parent)
        self.ui_item.Create(parent, choices=[choice.label for choice in self.choices])
        # self.ui_item.SetSizeHints((self._min_width, -1))
        # self._make_bindings()
        self._init()
        return self
