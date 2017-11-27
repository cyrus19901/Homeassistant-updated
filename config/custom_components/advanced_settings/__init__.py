"""
The "advanced settings" component.

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

DOMAIN = "advanced_settings"
FROM = "from"
SCAN_INTERVAL = timedelta(3600)

DEPENDENCIES = []

def setup(hass, config):
    """Setup our skeleton component."""

    _LOGGER.info("Advanced Settings loading.")
    
    component = EntityComponent(_LOGGER, DOMAIN, hass, SCAN_INTERVAL)

    component.setup(config)

    descriptions = load_yaml_config_file(
        os.path.join(os.path.dirname(__file__), 'services.yaml'))

    def update_advanced_settings(service):
        """Do any update to the component."""
        
        update_obj = service.data.get('value')

        _LOGGER.info("update object: %s", update_obj)

        advanced_settings = hass.states.get('advanced_settings.advanced_settings').as_dict()
        attributes = advanced_settings["attributes"]

        update_value = update_obj["value"]
        target = update_obj["target"]
        subtarget = update_obj["subtarget"]

        _LOGGER.info("subtarget: %s", subtarget)

        if subtarget is not None:
            _LOGGER.info("before list")
            if subtarget == "list":
                _LOGGER.info("in list")
                _LOGGER.info("before update list: %s", attributes[target][subtarget])
                _LOGGER.info("before value: %s", update_value)

                listindex = update_obj["listindex"]
                listtarget = update_obj["listtarget"]

                _LOGGER.info("before listtarget: %s", listtarget)

                _LOGGER.info("before index: %s", listindex)
                _LOGGER.info("before list index: %s", attributes[target][subtarget][listindex])

                attributes[target][subtarget][listindex][listtarget] = update_value

                _LOGGER.info("after update: %s", attributes[target][subtarget])
            else:
                _LOGGER.info("in else branch")
                attributes[target][subtarget] = update_value
        else:
            attributes[target] = update_value

        hass.states.set('advanced_settings.advanced_settings', 'On', attributes, True)

        _LOGGER.info("advanced settings after update: %s", hass.states.get('advanced_settings.advanced_settings'))

    hass.services.register(
        DOMAIN,
        'update_advanced_settings',
        update_advanced_settings,
        descriptions['update_advanced_settings'])

    return True


class AdvancedSettingsComponent(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""

        _LOGGER.info("AdvancedSettingsPlatform loading.")

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Advanced Settings'

    @property
    def state(self):
        """Card state."""
        return 'happy'

    @property
    def state_attributes(self):
        """Return the optional state attributes."""

        data = {
            "energySavings":{
                "label": "",
                "value": 11,
                "units": "kWh"
            },
            "powerSavings": {
                "label": "",
                "value": 9,
                "units": "kW"
            },
            "timePeriodStart": {
                "value": "01/01/2017"
            },
            "timePeriodEnd": {
                "value": "12/31/2017"
            },
            "savingsStartTime": {
                "value": "2017-10-24T10:00:00-07:00"
            },
            "savingsEndTime": {
                "value": "2017-10-24T17:00:00-07:00"
            },
            "incentives": {
                "label": "Incentives",
                "value": 10,
                "units": "$ per peak period"
            },
            "time_of_use_pricing": {
                "label": "Time of use pricing",
                "list": [
                    {
                        "startTime": "2017-10-24T10:00:00-07:00",
                        "endTime": "2017-10-24T14:00:00-07:00",
                        "value": 15,
                        "units": "cents per"
                    },
                    {
                        "startTime": "2017-10-24T14:00:00-07:00",
                        "endTime": "2017-10-24T20:00:00-07:00",
                        "value": 35,
                        "units": "cents per"
                    },
                    {
                        "startTime": "2017-10-24T20:00:00-07:00",
                        "endTime": "2017-10-24T09:00:00-07:00",
                        "value": 10,
                        "units": "cents per"
                    },
                ]
            }
        }

        return data
