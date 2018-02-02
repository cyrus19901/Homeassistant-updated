"""
The "shortcut adder" component.

"""

import asyncio
import logging
import os
import json
from datetime import timedelta
from homeassistant.config import load_yaml_config_file
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.core import State


_LOGGER = logging.getLogger(__name__)

DOMAIN = "shortcut_adder"
FROM = "from"
SCAN_INTERVAL = timedelta(3600)

DEPENDENCIES = []

def setup(hass, config):
    """Setup our skeleton component."""

    _LOGGER.info("shortcut adder loading.")
    
    component = EntityComponent(_LOGGER, DOMAIN, hass, SCAN_INTERVAL)

    component.setup(config)

    descriptions = load_yaml_config_file(
        os.path.join(os.path.dirname(__file__), 'services.yaml'))

    def update_shortcut_adder(service):
        """Update the shortcut adder setting."""

        update_obj = service.data.get('value')

        _LOGGER.info("update_obj: %s", update_obj)

        update_value = update_obj["value"]

        shortcut_adder = hass.states.get('shortcut_adder.shortcut_adder').as_dict()

        attributes = shortcut_adder["attributes"]

        _LOGGER.info("before update: %s", attributes)
        _LOGGER.info("update value: %s", update_value)

        attributes["added_shortcuts"] = update_value

        _LOGGER.info("after update: %s", attributes)

        hass.states.set('shortcut_adder.shortcut_adder', 'connected_homes', attributes, True)

    hass.services.register(
        DOMAIN,
        'update_shortcut_adder',
        update_shortcut_adder,
        descriptions['update_shortcut_adder'])

    return True


class ShortcutAdderComponent(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""

        _LOGGER.info("ShortcutAdderPlatform loading.")

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'shortcut adder'

    @property
    def state(self):
        """shortcut adder state."""
        return 'happy'

    @property
    def state_attributes(self):
        """Return the optional state attributes."""

        data = {
            "added_shortcuts": []
        }

        return data
