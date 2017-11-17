"""
The "energy efficiency platform" platform.

"""

import logging
from custom_components.energy_efficiency import EnergyEfficiencyComponent

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""

    _LOGGER.info("Setting up EnergyEfficiencyPlatform.")

    add_devices([EnergyEfficiencyPlatform()])


class EnergyEfficiencyPlatform(EnergyEfficiencyComponent):
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
        return 'Peak Period Energy and Compensation'

    def set_energy_efficiency(self: EnergyEfficiencyComponent, new_value):
        _LOGGER.info("In component set_energy_efficiency method")
        # _LOGGER.info("slider value: %s", new_value)
        # self._state = {'slider_value': new_value.slider_value}
        # _LOGGER.info("state: %s", self._state)
        # self.state_attributes["device"][0]["flexibility"] = new_value
        # _LOGGER.info("energy efficiency component device flexibility: %s", self.state_attributes["device"][0]["flexibility"])

