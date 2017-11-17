"""
The "energy efficiency" component.

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

DOMAIN = "energy_efficiency"
FROM = "from"
SCAN_INTERVAL = timedelta(3600)

DEPENDENCIES = []

def setup(hass, config):
    """Setup our skeleton component."""

    _LOGGER.info("Energy Efficiency loading.")
    
    component = EntityComponent(_LOGGER, DOMAIN, hass, SCAN_INTERVAL)

    component.setup(config)

    descriptions = load_yaml_config_file(
        os.path.join(os.path.dirname(__file__), 'services.yaml'))

    def update_energy_efficiency(service):
        """Do any update to the component."""
        # _LOGGER.info("energy efficiency service object: %s", service)
        # _LOGGER.info("what is in here?: %s", hass)

        update_obj = service.data.get('value')

        _LOGGER.info("update object: %s", update_obj)

        update_value = update_obj["value"]
        target = update_obj["target"]
        subtarget = update_obj["subtarget"]

        _LOGGER.info("before energy_efficiency")

        energy_efficiency = hass.states.get('energy_efficiency.peak_period_energy_and_compensation').as_dict()

        _LOGGER.info("after energy_efficiency: %s", energy_efficiency)
        
        attributes = energy_efficiency["attributes"]

        _LOGGER.info("before update: %s", attributes[target][subtarget])

        attributes[target][subtarget] = update_value
        
        _LOGGER.info("after update: %s", attributes[target][subtarget])

        energy_efficiency["attributes"] = attributes

        hass.states.set('energy_efficiency.peak_period_energy_and_compensation', 'On', attributes, True)

    hass.services.register(
        DOMAIN,
        'update_energy_efficiency',
        update_energy_efficiency,
        descriptions['update_energy_efficiency'])

    return True


class EnergyEfficiencyComponent(Entity):
    """Representation of a Component."""

    def __init__(self):
        """Initialize the component."""

        _LOGGER.info("EnergyEfficiencyPlatform loading.")

    @property
    def name(self):
        """Return the name of the component."""
        return 'Energy Efficiency'

    @property
    def state(self):
        """Component state."""
        return 'happy'

    @property
    def state_attributes(self):
        """Return the optional state attributes."""

        data = {
            "energyReductionEstimate":{
                "value": "7",
                "units": "kwh"
            },
            "energyReductionGoal":{
                "value": "9",
                "units": "kwh"
            },
            "energyReductionActual":{
                "value": "8",
                "units": "kwh"
            },
            "compensationEstimate":{
                "value": "$7"
            },
            "compensationGoal":{
                "value": "$8"
            },
            "compensationActual":{
                "value": "$6"
            },
            "useAlgorithm": {
                "value": True
            }
        }

        return data
