"""
The "whole-house energy" component.

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

DOMAIN = "whole_house_energy"
FROM = "from"
SCAN_INTERVAL = timedelta(3600)

DEPENDENCIES = []

def setup(hass, config):
    """Setup our skeleton component."""

    _LOGGER.info("Whole-House Energy loading.")
    
    component = EntityComponent(_LOGGER, DOMAIN, hass, SCAN_INTERVAL)

    component.setup(config)

    descriptions = load_yaml_config_file(
        os.path.join(os.path.dirname(__file__), 'services.yaml'))

    def update_whole_house_energy(service):
        """Do any update to the component."""
        # _LOGGER.info("whole-house energy service object: %s", service)
        # _LOGGER.info("what is in here?: %s", hass)

        update_obj = service.data.get('value')

        _LOGGER.info("update object: %s", update_obj)

        update_value = update_obj["value"]
        target = update_obj["target"]
        subtarget = update_obj["subtarget"]

        _LOGGER.info("before whole_house_energy")

        whole_house_energy = hass.states.get('whole_house_energy.whole_house_energy').as_dict()

        _LOGGER.info("after whole_house_energy: %s", whole_house_energy)
        
        attributes = whole_house_energy["attributes"]

        _LOGGER.info("before update: %s", attributes[target][subtarget])

        attributes[target][subtarget] = update_value
        
        _LOGGER.info("after update: %s", attributes[target][subtarget])

        # whole_house_energy["attributes"] = attributes

        hass.states.set('whole_house_energy.whole_house_energy', 'connected_homes', attributes, True)

    hass.services.register(
        DOMAIN,
        'update_whole_house_energy',
        update_whole_house_energy,
        descriptions['update_whole_house_energy'])

    return True


class WholeHouseEnergyComponent(Entity):
    """Representation of a Component."""

    def __init__(self):
        """Initialize the component."""

        _LOGGER.info("WholeHouseEnergyPlatform loading.")

    @property
    def name(self):
        """Return the name of the component."""
        return 'Whole-House Energy'

    @property
    def state(self):
        """Component state."""
        return 'happy'

    @property
    def state_attributes(self):
        """Return the optional state attributes."""

        data = {
            "ppReductionEstimate":{
                "value": "7",
                "units": "kWh"
            },
            "ppReductionGoal":{
                "value": "9",
                "units": "kWh"
            },
            "touReductionEstimate":{
                "value": "10",
                "units": "kWh"
            },
            "touReductionGoal":{
                "value": "15",
                "units": "kWh"
            },
            "ppBenefitEstimate":{
                "value": "$0.70"
            },
            "ppBenefitGoal":{
                "value": "$0.90"
            },
            "touBenefitEstimate":{
                "value": "$1"
            },
            "touBenefitGoal":{
                "value": "$1.50"
            },
            "useAlgorithm": {
                "value": True
            },
            "goalLegendLabel": "goal (from utility)",
            "canToggle": True
        }

        return data
