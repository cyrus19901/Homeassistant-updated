"""
The "device statuses" component.

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

DOMAIN = "device_statuses"
FROM = "from"
SCAN_INTERVAL = timedelta(3600)

DEPENDENCIES = []

def setup(hass, config):
    """Setup our skeleton component."""

    _LOGGER.info("Device Statuses loading.")
    
    component = EntityComponent(_LOGGER, DOMAIN, hass, SCAN_INTERVAL)

    component.setup(config)

    descriptions = load_yaml_config_file(
        os.path.join(os.path.dirname(__file__), 'services.yaml'))

    def update_device_statuses(service):
        """Update device statuses."""

        update_obj = service.data.get('value')

        device_statuses = hass.states.get('device_statuses.device_statuses').as_dict()
        
        attributes = device_statuses["attributes"]

        for obj in update_obj:
            attributes["devices"][obj["device"]][obj["target"]] = obj["value"]

        device_statuses["attributes"] = attributes

        hass.states.set('device_statuses.device_statuses', 'On', attributes, True)

    hass.services.register(
        DOMAIN,
        'update_device_statuses',
        update_device_statuses,
        descriptions['update_device_statuses'])

    def update_chart_type(service):
        """Switch to line chart or bar chart."""

        update_obj = service.data.get('value')

        _LOGGER.info("updating chart type")
        _LOGGER.info("update_obj: %s", update_obj)

        device_statuses = hass.states.get('device_statuses.device_statuses').as_dict()
        
        attributes = device_statuses["attributes"]

        for obj in update_obj:
            _LOGGER.info("in for obj in update_obj loop")
            for series in attributes["chartSeries"]:
                _LOGGER.info("in for series in attributes loop")
                _LOGGER.info("series id: %s", series["id"])
                _LOGGER.info("obj value: %s", obj["id"])
                if series["id"] == obj["id"]:
                    _LOGGER.info("found the right series")
                    series["type"] = obj["value"]

        device_statuses["attributes"] = attributes

        hass.states.set('device_statuses.device_statuses', 'On', attributes, True)

    hass.services.register(
        DOMAIN,
        'update_chart_type',
        update_chart_type,
        descriptions['update_chart_type'])

    return True


class DeviceStatusesComponent(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""

        _LOGGER.info("DeviceStatusesPlatform loading.")

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Device Statuses'

    @property
    def state(self):
        """Camera state."""
        return 'happy'

    @property
    def state_attributes(self):
        """Return the optional state attributes."""

        data = {
            "chartSeries": [
                {
                    "data": {
                        "times": [
                            '2017-07-17 23:36:58.368599Z',
                            '2017-07-17 23:37:28.368599Z',
                            '2017-07-17 23:37:58.368599Z',
                            '2017-07-17 23:38:28.368599Z',
                            '2017-07-17 23:38:58.368599Z',
                            '2017-07-17 23:39:28.368599Z',
                            '2017-07-17 23:39:58.368599Z',
                            '2017-07-17 23:40:28.368599Z',
                            '2017-07-17 23:40:58.368599Z',
                            '2017-07-17 23:41:28.368599Z'
                        ],
                        "time-format": "h:mm a",
                        "series": {
                            "AC1": { 
                                "points": [ 3, 4, 6, 5, 3, 4, 4, 5, 4, 5 ]
                            },
                            "AC2": { 
                                "points": [ 4, 5, 5, 4, 3, 5, 6, 2, 6, 6 ]
                            },
                            "WH1": { 
                                "points": [ 3, 2, 3, 6, 5, 5, 3, 3, 3, 2 ]
                            }
                        }
                    },
                    "type": "bar",
                    "label": "Energy (kWh)",
                    "id": "device-energy",
                    "updateMethod": "update_chart_type"
                },
                {
                    "data": {
                        "times": [
                            '2017-07-17 23:36:58.368599Z',
                            '2017-07-17 23:37:28.368599Z',
                            '2017-07-17 23:37:58.368599Z',
                            '2017-07-17 23:38:28.368599Z',
                            '2017-07-17 23:38:58.368599Z',
                            '2017-07-17 23:39:28.368599Z',
                            '2017-07-17 23:39:58.368599Z',
                            '2017-07-17 23:40:28.368599Z',
                            '2017-07-17 23:40:58.368599Z',
                            '2017-07-17 23:41:28.368599Z'
                        ],
                        "time-format": "h:mm a",
                        "series": {
                            "AC1": { 
                                "points": [ 3, 4, 2, 2, 6, 5, 5, 4, 3, 5 ],
                                "time-format": "h:mm a"
                            },
                            "AC2": { 
                                "points": [ 7, 6, 7, 5, 4, 4, 2, 2, 3, 6 ],
                                "time-format": "h:mm a"
                            },
                            "WH1": { 
                                "points": [ 5, 3, 3, 2, 3, 5, 4, 6, 6, 3 ],
                                "time-format": "h:mm a"
                            }
                        }
                    },
                    "type": "bar",
                    "label": "Power (kW)",
                    "id": "device-power",
                    "updateMethod": "update_chart_type"
                }
            ]
        }

        return data
