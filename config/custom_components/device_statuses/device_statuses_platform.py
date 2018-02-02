"""
The "device statuses platform" platform.

"""

import logging
from custom_components.device_statuses import DeviceStatusesComponent

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""

    _LOGGER.info("Setting up DeviceStatusesPlatform.")

    add_devices([DeviceStatusesPlatform()])


class DeviceStatusesPlatform(DeviceStatusesComponent):
    """Representation of the device statuses platform."""

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
        return 'Device Statuses'

