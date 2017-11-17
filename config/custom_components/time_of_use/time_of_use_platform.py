"""
The "time of use platform" platform.

"""

import logging
from custom_components.time_of_use import TimeOfUseComponent

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""

    _LOGGER.info("Setting up TimeOfUsePlatform.")

    add_devices([TimeOfUsePlatform()])


class TimeOfUsePlatform(TimeOfUseComponent):
    """Representation of a demo climate device."""

    def __init__(self):
        """Initialize the climate device."""
        self._state = 'On'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Time of use energy and savings'

    def set_time_of_use(self: TimeOfUseComponent, new_value):
        _LOGGER.info("In component set_time_of_use method")
        # _LOGGER.info("slider value: %s", new_value)
        # self._state = {'slider_value': new_value.slider_value}
        # _LOGGER.info("state: %s", self._state)
        # self.state_attributes["device"][0]["flexibility"] = new_value
        # _LOGGER.info("time of use component device flexibility: %s", self.state_attributes["device"][0]["flexibility"])

