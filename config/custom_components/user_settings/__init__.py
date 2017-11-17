"""
The "user settings" component.

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

DOMAIN = "user_settings"
FROM = "from"
SCAN_INTERVAL = timedelta(3600)

DEPENDENCIES = []

def setup(hass, config):
    """Setup our skeleton component."""

    _LOGGER.info("User Settings loading.")
    
    component = EntityComponent(_LOGGER, DOMAIN, hass, SCAN_INTERVAL)

    component.setup(config)

    descriptions = load_yaml_config_file(
        os.path.join(os.path.dirname(__file__), 'services.yaml'))

    def update_user_settings(service):
        """Update a user setting."""

        update_obj = service.data.get('value')

        _LOGGER.info("update_obj: %s", update_obj)

        target_device = update_obj["device"]
        target_setting = update_obj["setting"]
        target_attr = update_obj["attr"]
        update_value = update_obj["value"]

        user_settings = hass.states.get('user_settings.user_settings').as_dict()

        _LOGGER.info("updating user settings: %s", user_settings)
        
        attributes = user_settings["attributes"]

        _LOGGER.info("updating attributes: %s", attributes)

        found_device = attributes["devices"][target_device]
        _LOGGER.info("found device: %s", found_device)

        for s in found_device["settings"]:
            if s["name"] == target_setting:
                found_setting = s

                _LOGGER.info("found setting: %s", found_setting)

                for a in found_setting["attributes"]:
                    if a["name"] == target_attr:
                        found_attr = a

                        _LOGGER.info("found attribute: %s", found_attr)

                        found_attr["value"] = update_value
                        break
                break

        _LOGGER.info("after update: %s", attributes)

        hass.states.set('user_settings.user_settings', 'On', attributes, True)

    hass.services.register(
        DOMAIN,
        'update_user_settings',
        update_user_settings,
        descriptions['update_user_settings'])

    return True


class UserSettingsComponent(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""

        _LOGGER.info("UserSettingsPlatform loading.")

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'User Settings'

    @property
    def state(self):
        """Camera state."""
        return 'happy'

    @property
    def overall_reduction(self):
        """Return the name of the sensor."""
        return 84

    @property
    def state_attributes(self):
        """Return the optional state attributes."""

        data = {
            "devices": {
                "AC1":  {
                    "settings": [
                        {
                            "name": "preferred_temperature",
                            "label": "Preferred",
                            "type": "",
                            "attributes": [
                                {
                                    "name": "temperature",
                                    "type": "number",
                                    "units": "F",
                                    "value": 75
                                }
                                
                            ]
                        },  
                        {
                            "name": "active_setback",
                            "label": "Active Setback",
                            "type": "range",
                            "attributes": [
                                {
                                    "name": "min",
                                    "type": "number",
                                    "units": "F",
                                    "value": 65
                                },
                                {
                                    "name": "max",
                                    "type": "number",
                                    "units": "F",
                                    "value": 80
                                }
                            ]
                        }       
                    ]
                },
                "AC2": {
                    "settings": [
                        {
                            "name": "preferred",
                            "label": "Preferred",
                            "type": "",
                            "attributes": [
                                {
                                    "name": "temperature",
                                    "type": "number",
                                    "units": "F",
                                    "value": 78
                                }
                                
                            ]
                        },
                        {
                            "name": "active_setback",
                            "label": "Active Setback",
                            "type": "range",
                            "attributes": [
                                {
                                    "name": "min",
                                    "type": "number",
                                    "units": "F",
                                    "value": 65
                                },
                                {
                                    "name": "max",
                                    "type": "number",
                                    "units": "F",
                                    "value": 80
                                }
                            ]
                        }           
                    ]
                },
                "WH1": {
                    "settings": [
                        {
                            "name": "max",
                            "label": "Max",
                            "type": "",
                            "attributes": [
                                {
                                    "name": "temperature",
                                    "type": "number",
                                    "units": "F",
                                    "value": 150
                                }
                                
                            ]
                        },
                        {
                            "name": "shower_time",
                            "label": "Shower Time",
                            "type": "list",
                            "attributes": [
                                {
                                    "name": "0",
                                    "type": "time",
                                    "value": "2017-10-24T10:00:00-07:00"
                                },
                                {
                                    "name": "1",
                                    "type": "time",
                                    "value": "2017-10-24T17:00:00-07:00"
                                }
                            ]
                        }           
                    ]
                },
                "EV": {
                    "settings": [
                        {
                            "name": "charging_time",
                            "label": "Charging Time",
                            "type": "range",
                            "attributes": [
                                {
                                    "name": "start",
                                    "type": "time",
                                    "value": "2017-10-24T10:00:00-07:00"
                                },
                                {
                                    "name": "end",
                                    "type": "time",
                                    "value": "2017-10-24T14:00:00-07:00"
                                }
                            ]
                        }       
                    ]
                }
            }
        }

        return data
