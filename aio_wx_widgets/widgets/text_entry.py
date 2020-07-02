import logging
from typing import Union, Optional
import string
import wx

from aio_wx_widgets.binding import Bindable

_LOGGER = logging.getLogger(__name__)


class IntValidator(wx.Validator):
    """Validator."""

    def __init__(self):
        """Init."""
        wx.Validator.__init__(self)
        self.Bind(wx.EVT_CHAR, self._on_char)

    def Clone(self):
        """Clone."""
        return IntValidator()

    def _on_char(self, event):
        value = event.GetKeyCode()

        if chr(value) in string.digits:
            event.Skip()
            return
        return

    def Validate(self, win):
        """Validate."""
        ctrl = self.GetWindow()
        value = ctrl.GetValue()
        try:
            int(value)
        except ValueError:
            return False
        return True


class IntEntry(Bindable):
    """A textctrl for putting in integers.

    The value property exposes this integer value.
    """

    def __init__(
        self,
        label: Union[None, int, str] = None,
        parent=None,
        multiline=False,
        binding=None,
    ):
        super().__init__(binding[0], binding[1])
        self.value: Optional[int] = None
        self._txt = text_ctrl(
            label=label, parent=parent, multiline=multiline, validator=IntValidator()
        )
        self._parent = parent

    def _set_value(self, value):
        self._txt.SetValue(str(value))

    def __call__(self, parent):
        self._txt = self._txt(parent)
        self._txt.Bind(wx.EVT_TEXT, self._on_text)
        self._make_binding()

        return self._txt

    def _on_text(self, evt):
        _LOGGER.debug("Data entered")
        if self._fire_update_event:
            _LOGGER.debug("Firing update")
            self.value = int(evt.GetString())
            setattr(self._obj, self._property, self.value)
        self._fire_update_event = True


def text_ctrl(
    label=None, parent=None, multiline=False, validator=wx.DefaultValidator,
):
    """Create a wx text control."""
    txt = wx.TextCtrl()
    style = 0
    if multiline:
        style = style | wx.TE_MULTILINE

    def _create(parent):
        args = {"style": style, "validator": validator}
        if label:
            args["value"] = str(label)

        txt.Create(parent, **args)
        return txt

    if parent:
        return _create(parent)
    return _create
