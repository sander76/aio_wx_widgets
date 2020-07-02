import logging

_LOGGER = logging.getLogger(__name__)

# PROPERTY_DICT = "_property_dict_"
WATCHERS = "_watchers"
#
# def prop_setter(key):
#     def _setter(self, value):
#
#         if PROPERTY_DICT not in self.__dict__:
#             self.__dict__[PROPERTY_DICT] = {}
#         _LOGGER.debug("Settin property %s to value %s", key, value)
#         self.__dict__[PROPERTY_DICT][key] = value
#
#         if property_watch_list_key not in self.__dict__[PROPERTY_DICT]:
#             self.__dict__[PROPERTY_DICT][property_watch_list_key] = []
#
#         watch_list = self.__dict__[PROPERTY_DICT][property_watch_list_key]
#
#         _LOGGER.debug(
#             "Setting %s to %s # of subscribers %s", key, value, len(watch_list)
#         )
#
#         for prop in watch_list:
#             prop(value)
#
#     return _setter

#
# def prop_getter(key):
#     def _getter(self):
#         _LOGGER.debug("Getting value for %s", key)
#         return self.__dict__[PROPERTY_DICT][key]
#
#     return _getter


class Bindable:
    def __init__(self, bind_object, bind_property):
        self._obj = bind_object
        self._property = bind_property
        self._fire_update_event = True

    def _set_ui_value(self, value):
        raise NotImplementedError()

    def _make_binding(self):
        if WATCHERS not in self._obj.__dict__:
            self._obj.__dict__[WATCHERS] = {}
        if self._property not in self._obj.__dict__[WATCHERS]:
            _LOGGER.debug("No watchers yet for %s", self._property)
            self._obj.__dict__[WATCHERS][self._property] = []
        self._obj.__dict__[WATCHERS][self._property].append(self.update)

        value = getattr(self._obj, self._property)

        self._set_ui_value(value)

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
