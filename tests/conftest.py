import pytest

from aio_wx_widgets.controller import BaseController


@pytest.fixture
def base_model():
    class Model:
        """A simple model"""

    return Model()


@pytest.fixture
def base_controller(base_model):
    return BaseController(model=base_model)
