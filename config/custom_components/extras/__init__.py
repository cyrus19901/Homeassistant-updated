"""
The "extras" component.

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

DOMAIN = "extras"
FROM = "from"
SCAN_INTERVAL = timedelta(3600)

DEPENDENCIES = []

def setup(hass, config):
    """Setup our skeleton component."""

    _LOGGER.info("Extras loading.")
    
    component = EntityComponent(_LOGGER, DOMAIN, hass, SCAN_INTERVAL)

    component.setup(config)

    descriptions = load_yaml_config_file(
        os.path.join(os.path.dirname(__file__), 'services.yaml'))

    def update_extras(service):
        """Update the extras setting."""

        update_obj = service.data.get("value")
        extras = hass.states.get('extras.extras').as_dict()
        attributes = extras["attributes"]

        _LOGGER.info("before update: %s", attributes)

        _LOGGER.info("update_obj: %s", update_obj)

        if "new" in update_obj:
            _LOGGER.info("handling new")

            _LOGGER.info("new id: %s", update_obj["new"]["id"])

            targetIndex = find_item_index(update_obj["new"]["id"], attributes["extra_items"])

            if targetIndex == -1:
                attributes["extra_items"].append(update_obj["new"])

        elif "remove" in update_obj:
            _LOGGER.info("handling remove")

            _LOGGER.info("remove id: %s", update_obj["remove"]["id"])

            targetIndex = find_item_index(update_obj["remove"]["id"], attributes["extra_items"])

            if targetIndex > -1:
                del attributes["extra_items"][targetIndex]

        elif "edit" in update_obj:
            _LOGGER.info("handling edit")

            _LOGGER.info("new id: %s", update_obj["edit"]["id"])

            targetIndex = find_item_index(update_obj["edit"]["id"], attributes["extra_items"])

            if targetIndex > -1:
                attributes["extra_items"][targetIndex] = update_obj["edit"]
        
        _LOGGER.info("after update: %s", attributes)

        hass.states.set('extras.extras', 'connected_homes', attributes, True)

    hass.services.register(
        DOMAIN,
        'update_extras',
        update_extras,
        descriptions['update_extras'])

    return True

def find_item_index(targetItem, itemsList):
    targetIndex = -1

    for index, item in enumerate(itemsList):

        _LOGGER.info("index: %s", index)
        _LOGGER.info("item: %s", item)
        _LOGGER.info("item id: %s", item["id"])

        if targetItem == item["id"]:
            targetIndex = index
            break

    return targetIndex

class ExtrasComponent(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""

        _LOGGER.info("ExtrasPlatform loading.")

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Extras'

    @property
    def state(self):
        """Extras state."""
        return 'happy'

    @property
    def state_attributes(self):
        """Return the optional state attributes."""

        data = {
            "extra_items": [
                { 
                    "id": "pay_my_bill",
                    "name": "Pay My Bill",
                    "description": "Pay your electric bill online at the utility's website",
                    "url": "https://www.pge.com/en_US/residential/your-account/account-management/manage-your-account/manage-your-account.page",
                    "button": "Go",
                    "image": "pay_online.png",
                    "enabled": True,
                    "color": 'teal'
                },
                { 
                    "id": "report_electric_outage",
                    "name": "Report Electric Outage",
                    "description": "Report an electric outage to the utility",
                    "url": "https://m.pge.com/?WT.pgeac=Home_Outages#outages",
                    "button": "Go",
                    "image": "electric_outage.png",
                    "enabled": True,
                    "color": 'orange'
                },
                { 
                    "id": "report_gas_outage",
                    "name": "Report Gas Outage",
                    "description": "Report a gas outage to the utility",
                    "url": "https://www.pge.com/en_US/residential/outages/current-outages/gas-outages/gas-outages.page",
                    "button": "Go",
                    "image": "gas_outage.png",
                    "enabled": True,
                    "color": 'pink'
                },
                { 
                    "id": "rebates",
                    "name": "Rebates",
                    "description": "Find rebate offers from the utility",
                    "url": "https://marketplace.pge.com/?categoryId=94",
                    "button": "Go",
                    "image": "home_product.png",
                    "enabled": True,
                    "color": 'teal'
                }
            ]
        }

        return data
