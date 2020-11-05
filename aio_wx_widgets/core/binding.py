"""Property binding."""
from __future__ import annotations
import logging
from typing import NamedTuple, TYPE_CHECKING, Optional, Callable, Any

from aio_wx_widgets.core.validators import ValidationError

if TYPE_CHECKING:
    from aio_wx_widgets.controller import BaseController

_LOGGER = logging.getLogger(__name__)

WATCHERS = "_watchers_"


class Binding(NamedTuple):
    """Binding data."""

    bound_object: "BaseController"
    bound_property: "str"


class OneWayBindable:
    """A one way (read only) property binding.

    A bound UI will only receive values from a property. The ui itself is not able
    to update the property.
    """

    def __init__(self, binding: Optional[Binding], set_ui_value: Callable[[Any], None]):
        """Read only binding."""
        self._binding = binding
        self._set_ui_value = set_ui_value

    @property
    def binding(self):
        return self._binding

    def make_binding(self):
        """Create the binding."""
        if self._binding is None:
            _LOGGER.debug("No binding defined.")
            return

        if WATCHERS not in self._binding.bound_object.__dict__:
            self._binding.bound_object.__dict__[WATCHERS] = {}
        if (
            self._binding.bound_property
            not in self._binding.bound_object.__dict__[WATCHERS]
        ):
            _LOGGER.debug("No watchers yet for %s", self._binding.bound_property)
            self._binding.bound_object.__dict__[WATCHERS][
                self._binding.bound_property
            ] = []
        self._binding.bound_object.__dict__[WATCHERS][
            self._binding.bound_property
        ].append(self._update)

        value = self.get_property_value()
        if value is None:
            _LOGGER.debug(
                "Original property has value None %s", self._binding.bound_property
            )
            self._allow_none = True

        self._fire_update_event = False
        self._set_ui_value(value)

    def _update(self, value):
        """Called when a property changes from outside this control.

        Update the control with the new value
        """
        _LOGGER.debug("Updating entry with new value.")
        # self._fire_update_event = False
        self._set_ui_value(value)
        _LOGGER.debug("Updated.")

    def get_property_value(self):
        """Return the property value of the bound object.

        This would be the attribute defined in the controller.
        """
        return getattr(self._binding.bound_object, self._binding.bound_property)


class TwoWayBindable(OneWayBindable):
    """Base class for binding a property to a widget.

    Make a widget inherit from this. The binding property modifies the controller bound
    property adding a watcher and emitting change events.
    """

    def __init__(
        self,
        binding: Binding,
        get_ui_value,
        set_ui_value,
        display_error: Optional = None,
    ):

        super().__init__(binding, set_ui_value)

        # Flag to stop firing updates when a property value has changed.
        # Prevents infinite loop of updating the value and firing update events.
        self._fire_update_event = True
        self._allow_none = False
        self._get_ui_value = get_ui_value
        self._display_error = display_error

    def _set_property_value(self, value):
        setattr(self._binding.bound_object, self._binding.bound_property, value)

    def _update(self, value):
        """Called when a property changes from outside this control.

        Update the control with the new value
        """
        self._fire_update_event = False
        _LOGGER.debug("Setting fire event to False on %s", id(self))
        super()._update(value)

    def on_ui_change(self, *args, **kwargs):  # noqa
        """Callback when UI widget value changes by user input."""
        _LOGGER.debug("UI value changed on id %s", id(self))
        if not self._fire_update_event:
            _LOGGER.debug("Not updating bindings as fire_update_event is False")
            _LOGGER.debug("Setting fire event to True on %s", id(self))
            self._fire_update_event = True
            return
        _LOGGER.debug("Trigger the binding")

        self.update_binding()

        _LOGGER.debug("Firing update")

    def update_binding(self, force=False):
        """Update the binding property.

        Args:
            force: [bool] this will force the value to be cast into the value according
                to the validator.
        """
        try:
            val = self._get_ui_value(force)
        except ValidationError as err:
            if self._display_error:
                self._display_error(err)
        else:
            self._set_property_value(val)
            _LOGGER.debug("Setting fire event to True on %s", id(self))
            self._fire_update_event = True
