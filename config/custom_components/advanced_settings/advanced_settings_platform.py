"""
The "advanced settings platform" platform.

"""

import logging
from custom_components.advanced_settings import AdvancedSettingsComponent

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""

    _LOGGER.info("Setting up AdvancedSettingsPlatform.")

    add_devices([AdvancedSettingsPlatform()])


class AdvancedSettingsPlatform(AdvancedSettingsComponent):
    """Representation of the advanced settings platform."""

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
        return 'Utility Settings'

    def set_advanced_settings(self: AdvancedSettingsComponent, new_value):
        _LOGGER.info("In component set_advanced_settings method")
        # _LOGGER.info("slider value: %s", new_value)
        # self._state = {'slider_value': new_value.slider_value}
        # _LOGGER.info("state: %s", self._state)
        # self.state_attributes["device"][0]["flexibility"] = new_value
        # _LOGGER.info("advanced settings component device flexibility: %s", self.state_attributes["device"][0]["flexibility"])

