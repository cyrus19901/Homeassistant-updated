"""
The "shortcut adder platform" platform.

"""

import logging
from custom_components.shortcut_adder import ShortcutAdderComponent

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""

    _LOGGER.info("Setting up ShortcutAdderPlatform.")

    add_devices([ShortcutAdderPlatform()])


class ShortcutAdderPlatform(ShortcutAdderComponent):
    """Representation of the shortcut adder platform."""

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
        return 'shortcut adder'

