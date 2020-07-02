import logging

_LOGGER = logging.getLogger(__name__)

PROPERTY_DICT = "_property_dict_"


def prop_setter(key, property_watch_list_key):
    def _setter(self, value):

        if PROPERTY_DICT not in self.__dict__:
            self.__dict__[PROPERTY_DICT] = {}
        _LOGGER.debug("Settin property %s to value %s", key, value)
        self.__dict__[PROPERTY_DICT][key] = value

        if property_watch_list_key not in self.__dict__[PROPERTY_DICT]:
            self.__dict__[PROPERTY_DICT][property_watch_list_key] = []

        watch_list = self.__dict__[PROPERTY_DICT][property_watch_list_key]

        _LOGGER.debug(
            "Setting %s to %s # of subscribers %s", key, value, len(watch_list)
        )

        for prop in watch_list:
            prop(value)

    return _setter


def prop_getter(key):
    def _getter(self):
        _LOGGER.debug("Getting value for %s", key)
        return self.__dict__[PROPERTY_DICT][key]

    return _getter


class Bindable:
    def __init__(self, bind_object, bind_property):
        self._obj = bind_object
        self._property = bind_property
        self._attr_key = None
        self._fire_update_event = True
        self._attr_key = f"_{self._property}"
        self._property_watch_list_key = f"{self._attr_key}_watchers"

    def _set_ui_value(self, value):
        raise NotImplementedError()

    def _make_binding(self):
        if (
            PROPERTY_DICT not in self._obj.__dict__
            or self._attr_key not in self._obj.__dict__[PROPERTY_DICT]
        ):
            self._make_property(self._property_watch_list_key)

        watch_list = self._obj.__dict__[PROPERTY_DICT][self._property_watch_list_key]

        watch_list.append(self.update)
        value = getattr(self._obj, self._property)

        self._set_ui_value(value)

    def _make_property(self, property_watch_list_key):
        old_value = getattr(self._obj, self._property)

        _prop_setter = prop_setter(self._attr_key, property_watch_list_key)
        _prop_getter = prop_getter(self._attr_key)
        prop = property(_prop_getter, _prop_setter)

        setattr(self._obj.__class__, self._property, prop)

        self._set_property_value(old_value)

    def _set_property_value(self, value):
        setattr(self._obj, self._property, value)

    def update(self, value):
        """Called when a property changes from outside this control.

        Update the control with the new value
        """
        _LOGGER.debug("Updating entry with new value.")
        self._fire_update_event = False
        self._set_ui_value(value)

    def _on_ui_change(self, *args, **kwargs):
        _LOGGER.debug("UI value changed")
        if self._fire_update_event:
            _LOGGER.debug("Firing update")
            val = self._get_ui_value()
            self._set_property_value(val)
        self._fire_update_event = True

    def _get_ui_value(self):
        """Get the value from the ui widget."""
        raise NotImplementedError()
