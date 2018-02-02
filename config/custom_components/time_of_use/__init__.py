"""
The "time of use" component.

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

DOMAIN = "time_of_use"
FROM = "from"
SCAN_INTERVAL = timedelta(3600)

DEPENDENCIES = []

def setup(hass, config):
    """Setup our skeleton component."""

    _LOGGER.info("Time of Use loading.")
    
    component = EntityComponent(_LOGGER, DOMAIN, hass, SCAN_INTERVAL)

    component.setup(config)

    descriptions = load_yaml_config_file(
        os.path.join(os.path.dirname(__file__), 'services.yaml'))

    def update_time_of_use(service):
        """Do any update to the component."""
        
        update_obj = service.data.get('value')

        _LOGGER.info("update object: %s", update_obj)

        update_value = update_obj["value"]
        target = update_obj["target"]
        subtarget = update_obj["subtarget"]

        _LOGGER.info("before time_of_use")

        time_of_use = hass.states.get('time_of_use.time_of_use_energy_and_savings').as_dict()

        _LOGGER.info("after time_of_use: %s", time_of_use)
        
        attributes = time_of_use["attributes"]

        _LOGGER.info("before update: %s", attributes[target][subtarget])

        attributes[target][subtarget] = update_value
        
        _LOGGER.info("after update: %s", attributes[target][subtarget])

        time_of_use["attributes"] = attributes

        hass.states.set('time_of_use.time_of_use_energy_and_savings', 'connected_homes', attributes, True)

    hass.services.register(
        DOMAIN,
        'update_time_of_use',
        update_time_of_use,
        descriptions['update_time_of_use'])

    return True


class TimeOfUseComponent(Entity):
    """Representation of a Component."""

    def __init__(self):
        """Initialize the component."""

        _LOGGER.info("TimeOfUsePlatform loading.")

    @property
    def name(self):
        """Return the name of the component."""
        return 'Time of Use'

    @property
    def state(self):
        """Component state."""
        return 'happy'

    @property
    def state_attributes(self):
        """Return the optional state attributes."""

        data = {
            "energyReductionEstimate":{
                "value": "10",
                "units": "kWh"
            },
            "energyReductionGoal":{
                "value": "15",
                "units": "kWh"
            },
            # "energyReductionActual":{
            #     "value": "5",
            #     "units": "kwh"
            # },
            "savingsEstimate":{
                "value": "$1"
            },
            "savingsGoal":{
                "value": "$1.50"
            },
            # "savingsActual":{
            #     "value": "$5"
            # },
            "useAlgorithm": {
                "value": False
            },
            "goalLegendLabel": "goal (from customer)",
            "canToggle": False
        }

        return data
