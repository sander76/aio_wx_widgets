import logging

_LOGGER = logging.getLogger(__name__)


def prop_setter(key, property_watch_list):
    def _setter(self, value):
        _LOGGER.debug(
            "Setting %s to %s # of subscribers %s", key, value, len(property_watch_list)
        )

        self._property_dict_[key] = value
        for prop in property_watch_list:
            prop(value)

    return _setter


def prop_getter(key):
    def _getter(self):
        _LOGGER.debug("Getting value for %s", key)
        return self._property_dict_[key]

    return _getter


class Bindable:
    def __init__(self, bind_object, bind_property):
        self._obj = bind_object
        self._property = bind_property
        self._attr_key = None
        self._fire_update_event = True

    def _set_value(self, value):
        raise NotImplementedError()

    def _make_binding(self):
        self._attr_key = f"_{self._property}"
        property_watch_list_key = f"{self._attr_key}_watchers"

        if "_property_dict_" not in self._obj.__dict__:
            self._obj._property_dict_ = {}

        if property_watch_list_key not in self._obj._property_dict_:
            self._obj._property_dict_[property_watch_list_key] = []

        property_watch_list = self._obj._property_dict_[property_watch_list_key]

        if self._attr_key not in self._obj._property_dict_:
            _LOGGER.debug("property does not exist. Creating one.")
            self._make_property(property_watch_list)

        property_watch_list.append(self.update)
        value = getattr(self._obj, self._property)

        self._set_value(value)

    def _make_property(self, property_watch_list):
        old_value = getattr(self._obj, self._property)

        _prop_setter = prop_setter(self._attr_key, property_watch_list)
        _prop_getter = prop_getter(self._attr_key)
        prop = property(_prop_getter, _prop_setter)

        setattr(self._obj.__class__, self._property, prop)

        _prop_setter(self._obj, old_value)

    def update(self, value):
        """Called when a property changes from outside this control.

        Update the control with the new value
        """
        _LOGGER.debug("Updating entry with new value.")
        self._fire_update_event = False
        self._set_value(value)
