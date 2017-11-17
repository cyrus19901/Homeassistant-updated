"""
The "data privacy" component.

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

DOMAIN = "data_privacy"
FROM = "from"
SCAN_INTERVAL = timedelta(3600)

DEPENDENCIES = []

def setup(hass, config):
    """Setup our skeleton component."""

    _LOGGER.info("Data Privacy loading.")
    
    component = EntityComponent(_LOGGER, DOMAIN, hass, SCAN_INTERVAL)

    component.setup(config)

    descriptions = load_yaml_config_file(
        os.path.join(os.path.dirname(__file__), 'services.yaml'))

    def update_data_privacy(service):
        """Update the data privacy setting."""

        update_obj = service.data.get('value')

        _LOGGER.info("update_obj: %s", update_obj)

        update_value = update_obj["value"]

        data_privacy = hass.states.get('data_privacy.data_privacy').as_dict()

        attributes = data_privacy["attributes"]

        _LOGGER.info("before update: %s", attributes)
        _LOGGER.info("update value: %s", update_value)

        attributes["privacy_setting"] = update_value

        _LOGGER.info("after update: %s", attributes)

        hass.states.set('data_privacy.data_privacy', 'On', attributes, True)

    hass.services.register(
        DOMAIN,
        'update_data_privacy',
        update_data_privacy,
        descriptions['update_data_privacy'])

    return True


class DataPrivacyComponent(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""

        _LOGGER.info("DataPrivacyPlatform loading.")

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Data Privacy'

    @property
    def state(self):
        """Data privacy state."""
        return 'happy'

    @property
    def state_attributes(self):
        """Return the optional state attributes."""

        data = {
            "privacy_setting": "no_external",
            "privacy_options": [
                { 
                    "key": "no_external",
                    "label": "No external connections allowed. (most private)"
                },
                { 
                    "key": "vendor_updates",
                    "label": "Allow vendors to update your devices, but not share your data."
                },
                { 
                    "key": "allow_control",
                    "label": "Allow technicians and utilities to control devices for remote setup, diagnostics, and override. (least private)"
                }
            ]
        }

        return data
