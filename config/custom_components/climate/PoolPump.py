'''

Created on Aug, 2017
Implemented by Helia Zandi
email: zandih@ornl.gov

This material was prepared by UT-Battelle, LLC (UT-Battelle) under Contract DE-AC05-00OR22725
with the U.S. Department of Energy (DOE). All rights in the material are reserved by DOE on 
behalf of the Government and UT-Battelle pursuant to the contract. You are authorized to use
the material for Government purposes but it is not to be released or distributed to the public.
NEITHER THE UNITED STATES NOR THE UNITED STATES DEPARTMENT OF ENERGY, NOR UT-Battelle, NOR ANY
OF THEIR EMPLOYEES, MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR ASSUMES ANY LEGAL LIABILITY OR
RESPONSIBILITY FOR THE ACCURACY, COMPLETENESS, OR USEFULNESS OF ANY INFORMATION, APPARATUS, 
PRODUCT, OR PROCESS DISCLOSED, OR REPRESENTS THAT ITS USE WOULD NOT INFRINGE PRIVATELY OWNED RIGHTS.

'''

"""

    Shows communication between CTA-2045 module and a broker for PENTAIR Pool Pump
    
"""

import logging

import voluptuous as vol

import homeassistant.components.mqtt as mqtt

import homeassistant.components.CTA2045 as CTA2045

import homeassistant.loader as loader

from homeassistant.components.climate import (ClimateDevice,
    PLATFORM_SCHEMA, ATTR_TARGET_TEMP_HIGH, ATTR_TARGET_TEMP_LOW, STATE_AUX_HEAT, ATTR_CURRENT_TEMPERATURE)

from homeassistant.components.mqtt import (
    CONF_STATE_TOPIC, CONF_COMMAND_TOPIC, CONF_QOS, CONF_RETAIN)
    
from homeassistant.const import (
    CONF_NAME, CONF_MAC, TEMP_FAHRENHEIT, TEMP_CELSIUS, STATE_ON, STATE_OFF,
     STATE_UNKNOWN, ATTR_TEMPERATURE,STATE_CIRCULATE)

import homeassistant.helpers.config_validation as cv
from homeassistant.components import fan


DOMAIN = "CTA2045"
ENERGY_WATT_UNIT = "W & W-hr"
#OPERATION STATUS FOR sgd
STATE_IDLE_NORMAL = 'Idle_Normal'
STATE_RUNNING_NORMAL = 'Idle_running_Normal'
STATE_RUNNING_CURTAILED_GRID = 'Running_Curtailed_Grid'
STATE_RUNNING_HEIGTENED_GRID = 'Running_Heightened_Grid'
STATE_IDLE_GRID = 'Idle_Grid'
STATE_SGD_ERROR_CONDITION = 'SGD_Error_Condition'
STATE_UNUSED = 'Unused'

#DR commands
STATE_SHED = 'shed'
STATE_END_SHED = 'end_shed/event'
STATE_LOAD_UP = 'load_up'
STATE_CYCLING = 'cycling'
STATE_CRITICAL_PEAK_EVENT = 'critical_peak_event'
STATE_GRID_EMERGENCY = 'grid emergency'
STATE_POWER_LEVEL_10 = 'power_level_10%'
STATE_POWER_LEVEL_20 = 'power_level_20%'
STATE_POWER_LEVEL_30 = 'power_level_30%'
STATE_POWER_LEVEL_40 = 'power_level_40%'
STATE_POWER_LEVEL_50 = 'power_level_50%'
STATE_POWER_LEVEL_60 = 'power_level_60%'
STATE_POWER_LEVEL_70 = 'power_level_70%'
STATE_POWER_LEVEL_80 = 'power_level_80%'
STATE_POWER_LEVEL_90 = 'power_level_90%'


DEPENDENCIES = ['mqtt']

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'PENTAIR Pool Pump CTA2045 Module'
COMMON_TOPIC = 'devices/'
TOPIC = 'topic'


PLATFORM_SCHEMA = mqtt.MQTT_RW_PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup MQTT climate platform."""
    
    loader.get_component('CTA2045')
    mac_address = config.get(CONF_MAC)
    
    add_devices([PoolPumpClimate(
        hass,
        config.get(CONF_NAME),
        config.get(CONF_QOS),
        config.get(CONF_RETAIN),
        config.get(TOPIC, COMMON_TOPIC + mac_address + '/data'),
        mac_address,
    )])


class PoolPumpClimate(ClimateDevice):
    """Representation of a CTA- 2045 module for PENTAIR Pool Pump"""

    def __init__(self, hass, device_name, qos, retain, topic, mac_address):
        """Initialize the module"""
        
        self.device_name = device_name
        self.mac_address = mac_address
        self.qos = qos
        self.retain = retain
        self._hass = hass
        
        self.state_topic = COMMON_TOPIC + mac_address + '/data'
        self.command_topic = COMMON_TOPIC + mac_address + '/ctl/'
        topic = self.state_topic
        
        self.operation_mode_list_2 = [STATE_IDLE_NORMAL, STATE_RUNNING_NORMAL, STATE_RUNNING_CURTAILED_GRID, STATE_RUNNING_HEIGTENED_GRID, STATE_IDLE_GRID,
                                    STATE_SGD_ERROR_CONDITION, STATE_UNUSED]
        
        self.swing_mode_list_2 = [STATE_SHED, STATE_END_SHED,STATE_CRITICAL_PEAK_EVENT, STATE_GRID_EMERGENCY,
				                STATE_POWER_LEVEL_10, STATE_POWER_LEVEL_20, STATE_POWER_LEVEL_30, STATE_POWER_LEVEL_40, STATE_POWER_LEVEL_50,
				                STATE_POWER_LEVEL_60, STATE_POWER_LEVEL_70, STATE_POWER_LEVEL_80, STATE_POWER_LEVEL_90]
        
        self.CTA2045_module = CTA2045.CTA2045()
        
        self.mqqtDataReceived = False

        def data_received(topic, payload, qos):
            """A new message from MQTT module was received"""
           
            self.mqqtDataReceived = True
            self.CTA2045_module.parseJsonMessage(payload)
            self.schedule_update_ha_state()
        
        
        mqtt.subscribe(self._hass, self.state_topic, data_received, qos)


    @property
    def name(self):
        """Return the name of the module"""   
        return self.device_name

        
        
    @property
    def current_temperature(self):
        """Return the current temperature."""
        
        if self.mqqtDataReceived == False:
            return 0
        
        commodity = self.CTA2045_module.get_commodity_read()
        return commodity['cumulativeAmount']
    
    
    @property
    def temperature_unit(self):
        """Return the temperature unit, the default value is fahrenheit"""
        return TEMP_FAHRENHEIT


    @property
    def current_operation(self):
        """Return current mode of operation Idle normal, running normal, etc."""
        
        if self.mqqtDataReceived == False:
            return STATE_UNKNOWN
        
        cur_mode = self.CTA2045_module.get_operational_state()
        
        if cur_mode == 'Idle Normal':
            return STATE_IDLE_NORMAL
        elif cur_mode== 'Running Normal':
            return STATE_RUNNING_NORMAL
        elif cur_mode== 'Running Curtailed Grid':
            return STATE_RUNNING_CURTAILED_GRID
        elif cur_mode == 'Running Heightened Grid':
            return STATE_RUNNING_HEIGTENED_GRID
        elif cur_mode ==  'Idle Grid':
            return STATE_IDLE_GRID
        elif cur_mode ==   'SGD Error Condition':
            return STATE_SGD_ERROR_CONDITION
        elif cur_mode ==  'Unused':
            return STATE_UNUSED
        else:
            return STATE_UNKNOWN
        
        
        
    @property
    def operation_list(self):
        """List of available operation modes."""
        return self.operation_mode_list_2
    
    
    
    @property
    def current_swing_mode(self):
        """Return current DR event mode"""
        return STATE_UNKNOWN



    @property
    def target_temperature_low(self):
        """Return the temperature for cool set point"""
        
        if self.mqqtDataReceived == False:
            return 0
        
        commodity = self.CTA2045_module.get_commodity_read()
        return commodity['cumulativeAmount']



    @property
    def target_temperature_high(self):
        """Return the temperature for heat set point"""
        
        if self.mqqtDataReceived == False:
            return 0
        
        commodity = self.CTA2045_module.get_commodity_read()
        return commodity['cumulativeAmount']



    def set_swing_mode(self, swing_mode):
        """Set DR event."""
        swingMode = ''
        duration = 300

        if self.mqqtDataReceived == False:
            return

        if swing_mode ==  STATE_SHED:
            swingMode = 'shed'
            msg = self.CTA2045_module.set_load_shed(duration)
            msgJson = '"d":"{}"'.format(msg)
            mqtt.publish(self._hass, self.command_topic + "shedLoad", '{' + msgJson + '}', self.qos, self.retain)
            _LOGGER.debug("Send Shed load event for %s seconds", duration)

        elif swing_mode == STATE_END_SHED:
            swingMode = 'end_shed/event'
            msg = self.CTA2045_module.set_end_shed_load_cmd()
            msgJson = '"d":"{}"'.format(msg)
            mqtt.publish(self._hass, self.command_topic + "endShed", '{' + msgJson + '}', self.qos, self.retain)
            _LOGGER.debug("Send end Shed command")
            
#         elif swing_mode == STATE_LOAD_UP:
#             swingMode = 'load_up'
#         elif swing_mode == STATE_CYCLING:
#             swingMode= 'cycling'
        elif swing_mode ==  STATE_CRITICAL_PEAK_EVENT:
            swingMode= 'critical_peak_event'
            msg = self.CTA2045_module.set_critical_peak_demand(duration)
            msgJson = '"d":"{}"'.format(msg)
            mqtt.publish(self._hass, self.command_topic + "criticalPeakDemand", '{' + msgJson + '}', self.qos, self.retain)
            _LOGGER.debug("Send critical peak demand event for %s seconds", duration)
            
        elif swing_mode ==   STATE_GRID_EMERGENCY:
            swingMode = 'grid emergency'
            msg = self.CTA2045_module.set_grid_emergency(duration)
            msgJson = '"d":"{}"'.format(msg)
            mqtt.publish(self._hass, self.command_topic + "gridEmergency", '{' + msgJson + '}', self.qos, self.retain)
            _LOGGER.debug("Send grid emergency event for %s seconds", duration)
            
        elif swing_mode == STATE_POWER_LEVEL_10:
            swingMode = 'power_level_10%'
            msg = self.CTA2045_module.set_power_level(10)
            msgJson = '"d":"{}"'.format(msg)
            mqtt.publish(self._hass, self.command_topic + "powerLevel", '{' + msgJson + '}', self.qos, self.retain)
            _LOGGER.debug("Reduced power level by %10")
            
        elif swing_mode ==  STATE_POWER_LEVEL_20:
            swingMode = 'power_level_20%'
            msg = self.CTA2045_module.set_power_level(20)
            msgJson = '"d":"{}"'.format(msg)
            mqtt.publish(self._hass, self.command_topic + "powerLevel", '{' + msgJson + '}', self.qos, self.retain)
            _LOGGER.debug("Reduced power level by %20")
            
        elif swing_mode == STATE_POWER_LEVEL_30:
            swingMode= 'power_level_30%'
            msg = self.CTA2045_module.set_power_level(30)
            msgJson = '"d":"{}"'.format(msg)
            mqtt.publish(self._hass, self.command_topic + "powerLevel", '{' + msgJson + '}', self.qos, self.retain)
            _LOGGER.debug("Reduced power level by %30")
            
        elif swing_mode ==  STATE_POWER_LEVEL_40:
            swingMode= 'power_level_40%'
            msg = self.CTA2045_module.set_power_level(40)
            msgJson = '"d":"{}"'.format(msg)
            mqtt.publish(self._hass, self.command_topic + "powerLevel", '{' + msgJson + '}', self.qos, self.retain)
            _LOGGER.debug("Reduced power level by %40")
            
        elif swing_mode == STATE_POWER_LEVEL_50:
            swingMode = 'power_level_50%'
            msg = self.CTA2045_module.set_power_level(50)
            msgJson = '"d":"{}"'.format(msg)
            mqtt.publish(self._hass, self.command_topic + "powerLevel", '{' + msgJson + '}', self.qos, self.retain)
            _LOGGER.debug("Reduced power level by %50")
            
        elif swing_mode ==  STATE_POWER_LEVEL_60:
            swingMode = 'power_level_60%'
            msg = self.CTA2045_module.set_power_level(60)
            msgJson = '"d":"{}"'.format(msg)
            mqtt.publish(self._hass, self.command_topic + "powerLevel", '{' + msgJson + '}', self.qos, self.retain)
            _LOGGER.debug("Reduced power level by %60")
            
        elif swing_mode == STATE_POWER_LEVEL_70:
            swingMode= 'power_level_70%'
            msg = self.CTA2045_module.set_power_level(70)
            msgJson = '"d":"{}"'.format(msg)
            mqtt.publish(self._hass, self.command_topic + "powerLevel", '{' + msgJson + '}', self.qos, self.retain)
            _LOGGER.debug("Reduced power level by %70")
            
        elif swing_mode ==  STATE_POWER_LEVEL_80:
            swingMode= 'power_level_80%'
            msg = self.CTA2045_module.set_power_level(80)
            msgJson = '"d":"{}"'.format(msg)
            mqtt.publish(self._hass, self.command_topic + "powerLevel", '{' + msgJson + '}', self.qos, self.retain)
            _LOGGER.debug("Reduced power level by %80")
            
        elif swing_mode ==  STATE_POWER_LEVEL_90:
            swingMode= 'power_level_90%'
            msg = self.CTA2045_module.set_power_level(90)
            msgJson = '"d":"{}"'.format(msg)
            mqtt.publish(self._hass, self.command_topic + "powerLevel", '{' + msgJson + '}', self.qos, self.retain)
            _LOGGER.debug("Reduced power level by %90")
            
    
        self.schedule_update_ha_state()



    @property
    def swing_list(self):
        """List of available DR event mode."""
        return self.swing_mode_list_2
    

        
    
