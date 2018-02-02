"""
The "transactive platform" platform.

"""

import logging
from custom_components.transactive_home import TransactiveComponent

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""

    _LOGGER.info("Setting up TransactivePlatform.")

    add_devices([TransactivePlatform()])


class TransactivePlatform(TransactiveComponent):
    """Representation of the transactive home platform."""

    def __init__(self):
        """Initialize the platform."""
        self._state = 'connected_homes'

    @property
    def state(self):
        """Return the state of the platform."""
        return self._state

    @property
    def name(self):
        """Return the name of the platform."""
        return 'Transactive Home'

    def set_transactive_home(self: TransactiveComponent, new_value):
        _LOGGER.info("In component update_transactive_home method")
        _LOGGER.info("slider value: %s", new_value)
        # self._state = {'slider_value': new_value.slider_value}
        # _LOGGER.info("state: %s", self._state)
        self.state_attributes["device"][0]["flexibility"] = new_value
        _LOGGER.info("transactive component device flexibility: %s", self.state_attributes["device"][0]["flexibility"])

