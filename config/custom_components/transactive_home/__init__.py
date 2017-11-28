"""
The "transactive home" component.

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

DOMAIN = "transactive_home"
FROM = "from"
SCAN_INTERVAL = timedelta(3600)

DEPENDENCIES = []

def setup(hass, config):
    """Setup our skeleton component."""

    _LOGGER.info("Transacive Home loading.")
    
    component = EntityComponent(_LOGGER, DOMAIN, hass, SCAN_INTERVAL)

    component.setup(config)

    descriptions = load_yaml_config_file(
        os.path.join(os.path.dirname(__file__), 'services.yaml'))

    def update_transactive_home(service):
        """Do any update to the component."""
        
        update_obj = service.data.get('value')
        
        transactive_home = hass.states.get('transactive_home.transactive_home').as_dict()

        attributes = transactive_home["attributes"]

        # attributes["overallflexibility"][0][update_obj["target"]] = update_obj["value"]

        if update_obj["subtarget"] is not None:
            attributes[update_obj["target"]][update_obj["subtarget"]] = update_obj["value"]
        else:
            attributes[update_obj["target"]] = update_obj["value"]

        hass.states.set('transactive_home.transactive_home', State.from_dict(transactive_home), attributes, True)


    hass.services.register(
        DOMAIN,
        'update_transactive_home',
        update_transactive_home,
        descriptions['update_transactive_home'])

    return True


class TransactiveComponent(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""

        _LOGGER.info("TransactivePlatform loading.")

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Transactive Home'

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
            "progress_bar": {
                "message": "You're off to a good start.",
                "value": 55,
                "starting_point": 0,
                "end_point": 250,
                "last_year": 1680,
                "lastYearLabel": "Last year's total energy cost",
                "comparisonLabel": "savings compared to last year"
            },
            "overallflexibility":[{
                    "flexibility": 10,
                    "zone_min": 0,
                    "zone_max": 100
                }],
            "measures": [
                {
                    "label": "Overall Energy",
                    "value": 9.5,
                    "unit": "kWh"
                },
                {
                    "label": "Overall Power",
                    "value": 8.04,
                    "unit": "kW"
                }
            ],
            "chartSeries": [
                {
                    "data": {
                        "times": [
                            '2017-07-17 23:36:58.368599Z',
                            '2017-07-18 23:37:28.368599Z',
                            '2017-07-19 23:37:58.368599Z',
                            '2017-07-20 23:38:28.368599Z',
                            '2017-07-21 23:38:58.368599Z',
                            '2017-07-22 23:39:28.368599Z',
                            '2017-07-23 23:39:58.368599Z',
                            '2017-07-24 23:40:28.368599Z',
                            '2017-07-25 23:40:58.368599Z',
                            '2017-07-26 23:41:28.368599Z'
                        ],
                        "time-format": "MM/DD",
                        "series": {
                            "historical": {
                                "points": [ 3, 4, 6, 6, 7, 9, 11, 13, 16, 17 ],
                                "color": "#696969",
                                "line-style": "dash"
                            },
                            "actual": {
                                "points": [ 4, 5, 7, 8, None, None, None, None, None, None ],
                                "color": "#FF7F50",
                                "line-style": ""
                            },
                            "transactive": {
                                "points": [ 4, 5, 7, 8, 8, 8, 9, 9, 10, 12 ],
                                "color": "ForestGreen",
                                "line-style": "dash"
                            }
                        }
                    },
                    "type": "line",
                    "label": "Energy (kWh)",
                    "id": "transactive-home"
                }
            ]
        }

        return data
