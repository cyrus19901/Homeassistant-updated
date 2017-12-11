'''
Created on Nov 4, 2016
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

import json
import opcode
from math import sqrt

class CTA2045(object):
    '''
    This class provides communication with CTA- 2045 enabled devices
    The class includes method which are capable of encoding and decoding the json files received/sent from/to the devices
    '''

    def __init__(self):
        '''
        Constructor
        initializes the class variables
        '''
        self.flag = -1
        self.operationalState = ''
        self.endShed = 'unknown'
        self.shedEventDuration = {'Duration' : -1, 'Message' : ''}
        self.temperatureOffset = {'responseCode' : '', 'currentOffset' : 0, 'units' : ''}
        self.setPoints = {'responseCode' : '', 'deviceTypeSGD' : '', 'units' : '', 'setPoint1' : 0, 'setPoint2' : 0}
        self.curTemperature = {'responseCode' : '', 'deviceTypeSGD' : '', 'units' : '', 'temperature' : 0}
        self.commodityRead = {'responseCode' : '', 'commodityCode' : '', 'instantaneousRate' : 0, 'cumulativeAmount' : 0}
        self.thermostatMode = ''
        self.fanMode = {'fanMode' : '', 'responseCode' : ''}
        
   
    def get_flag_value(self):
        '''returns the value of flag'''
        
        return self.flag
    

    def get_operational_state(self):
        '''returns the value of operational state'''
        
        return self.operationalState


    def get_temperature_offset(self):
        '''returns the temperature offset values '''
        '''the variable keys are responseCode, currentOffset, units'''
        
        return self.temperatureOffset


    def get_setpoints(self):
        '''returns the value of setpoints'''
        '''the variable keys are responseCode, deviceTypeSGD, units, setPoint1, setPoint2'''
        
        return self.setPoints
    
    
    def get_curTemperature(self):
        '''returns the value for current temperature'''
        '''the variable keys are responseCode, deviceTypeSGD, units, temperature'''
        
        return self.curTemperature 
    
    
    def get_commodity_read(self):
        '''returns the value of commodity reads'''
        '''the variable keys are 'responseCode, commodityCode, instantaneousRate, cumulativeAmount'''
        
        return self.commodityRead
        
    
    def get_thermostat_mode(self): 
        '''returns the thermostat mode'''
        
        return self.thermostatMode
    
    
    def get_fanMode(self):
        '''returns the fan mode'''
        
        return self.fanMode
        
        
    def parseJsonMessage(self, jsonData):
            '''Parses the json file which contains the message sent by Emerson thermostat'''
  
            data = json.loads(jsonData)
     
            msg = data["d"]
     
            flagOver = msg[0:2]
            self.flag = 0 if (flagOver[0] == "0") else 1

            msg = msg[2:(len(msg))]   
            
            while(len(msg) > 0):
                
                '''read next 2 bytes'''
                
                msgType = msg[0:4]
                    
                if(msgType == "0801"):
                        
                    msg = self.parse0801MessageType(msg)
                        
                elif(msgType == "0802"):
                    
                    msg = self.parse0802MessageType(msg)
                else:
                    break;
                    
            print("Override Flag: " + str(self.flag), "Temperature: " + str(self.curTemperature['temperature']),"Heat Setpoint: " + str(self.setPoints['setPoint1']), "Cool Setpoint: " + str(self.setPoints['setPoint2']), "Units: " + self.curTemperature['units'], "Temperature Offset: " + str(self.temperatureOffset['currentOffset']))           
            print("responseCode: " + str(self.commodityRead['responseCode']), "commodityCode: " + str(self.commodityRead['commodityCode']), "instantaneousRate: " + str(self.commodityRead['instantaneousRate']), "cumulativeAmount: " + str(self.commodityRead['cumulativeAmount']))
            print("Load Shed Duration:" + str(self.shedEventDuration['Duration']), "Load Shed Message:" + self.shedEventDuration['Message'], "Load shed end: " + self.endShed )  
            print("*******************************************************************************************************************************************")                  
    
                        
    def parse0801MessageType(self,msg):
        '''Decodes the message based on 0x08, 0x01 message code for CTA 2045'''
        
        msg = msg[4: len(msg)]
        
        payLoadLen = int(msg[0:4],16)
        msg = msg[4: len(msg)]
        
        opcode1 = ""
        opcode2 = ""
        
        if payLoadLen == 0:
            return msg
         
        elif payLoadLen == 1:
            opcode1 = msg[0:2]
            msg = msg[2: len(msg)]
        else:
            opcode1 = msg[0:2]
            opcode2 = msg[2:4]
            msg = msg[4: len(msg)]
          
        ''' since Emerson thermostat only supports operational states, 
            the other messages are not checked by the code'''
            
        if opcode1 == "13":
            self.getOperationalState(opcode2)  
        elif opcode1 == "01":
            self.getShedEventDuration(opcode2) 
        elif opcode1 == "02":
            self.endShed = 'true'
        
        return msg
    
    
    def getShedEventDuration(self, opcode2):
        
        '''sets the shed event duration and message values'''
        self.endShed =  'false'
        
        if opcode2 == "00":
            self.shedEventDuration['Message'] = 'Duration is unknown'
            self.shedEventDuration['Duration'] = self.getEventDuration(opcode2)
        elif opcode2 == "FF":
            self.shedEventDuration['Message'] = 'Duration is longer that what can be represented'
            self.shedEventDuration['Duration'] = self.getEventDuration(opcode2)
        else:
            self.shedEventDuration['Message'] = 'Duration was computed successfully'
            self.shedEventDuration['Duration'] = self.getEventDuration(opcode2)
    
    
    def getEventDuration(self, opcode2):
        '''returns the value of event duration in seconds'''
        
        if opcode2 == "00":
            return -1
        elif opcode2 == "FF":
            return -1
        else:
            return( 2 * (float(opcode2) ** 2))
            
          
    def getOperationalState(self, opcode2):
        '''Provides the operational state of the device''' 
         
        if opcode2 == "00":
            self.operationalState = 'Idle Normal'
        elif opcode2 == "01":
            self.operationalState = 'Running Normal'
        elif opcode2 == "02":
            self.operationalState = 'Running Curtailed Grid'
        elif opcode2 == "03":
            self.operationalState = 'Running Heightened Grid'
        elif opcode2 == "04":
            self.operationalState = 'Idle Grid'
        elif opcode2 == "05":
            self.operationalState = 'SGD Error Condition'
        else:
            self.operationalState = 'Unused'
   
                  
    def parse0802MessageType(self,msg):   
        '''Decodes the message based on 0x08, 0x02 message code for CTA 2045'''                 
    
        msg = msg[4: len(msg)]
        
        payLoadLen = int(msg[0:4],16)
        opcode1 = msg[4:6]
        opcode2 = msg[6:8]
        msg = msg[8: len(msg)]
        payLoadLen = (payLoadLen - 2 ) * 2
        
        if opcode1 == "03":
            
            '''Get Temperature Offset, reply from SGD'''
            if opcode2 == "82":
                
                if payLoadLen >= 2 : self.temperatureOffset['responseCode'] = self.getResponseCode(msg[0:2])
                if payLoadLen >= 4 : self.temperatureOffset['currentOffset'] = int(msg[2:4],16)
                if payLoadLen >= 6 :
                    unit = int(msg[4:6],16)
                    self.temperatureOffset['units'] = 'F' if unit == 0 else 'C'
                msg = msg[payLoadLen : len(msg)]
            
            elif opcode2 == "83":
                '''Get setpoints, reply'''
                if payLoadLen >= 2 : self.setPoints['responseCode'] = self.getResponseCode(msg[0:2])
                if payLoadLen >= 6 : self.setPoints['deviceTypeSGD'] = self.getDeviceTypeSGD(msg[2:6])
                if payLoadLen >= 8 :
                    unit = int(msg[6:8],16)
                    self.setPoints['units'] = 'F' if unit == 0 else 'C'
                if payLoadLen >= 12 : self.setPoints['setPoint1'] = int(msg[8:12],16)
                if payLoadLen >= 16 : self.setPoints['setPoint2'] = int(msg[12:16],16)
                msg = msg[payLoadLen : len(msg)]
            
            elif opcode2 == "84":
                if payLoadLen >= 2 : self.curTemperature['responseCode'] = self.getResponseCode(msg[0:2])
                if payLoadLen >= 6 : self.curTemperature['deviceTypeSGD'] = self.getDeviceTypeSGD(msg[2:6])
                if payLoadLen >= 8 :
                    unit = int(msg[6:8],16)
                    self.curTemperature['units'] = 'F' if unit == 0 else 'C'
                if payLoadLen >= 12 : self.curTemperature['temperature'] = int(msg[8:12],16)
                msg = msg[payLoadLen : len(msg)]
                
        elif opcode1 == "06":
        
            '''Get/Set Commodity Read'''
            if opcode2 == "80":
                if payLoadLen >= 2 :  self.commodityRead['responseCode'] = self.getResponseCode(msg[0:2])
                if payLoadLen >= 4 :  self.commodityRead['commodityCode'] = self.getCommodityCode(msg[2:4])
                if payLoadLen >= 16 : self.commodityRead['instantaneousRate'] = int(msg[4:16],16)
                if payLoadLen >= 28 : self.commodityRead['cumulativeAmount'] = int(msg[16:28],16)
                msg = msg[payLoadLen : len(msg)]
                
        elif opcode1 == "07":
            
            if opcode2 == "81":
                '''Get thermostat mode'''
                if payLoadLen >= 2 : self.thermostatMode = self.getThermostatMode(msg[0:2])
                msg = msg[payLoadLen : len(msg)]
                
            elif opcode2 == "82":
                '''Get thermostat fan mode'''
                if payLoadLen >= 2 : self.fanMode['responseCode'] = self.getResponseCode(msg[0:2])
                if payLoadLen >= 4 : self.fanMode['fanMode'] = self.getFanMode(msg[2:4])
                msg = msg[payLoadLen : len(msg)]
                
        return msg
   
    
    def getResponseCode(self, resCode):
        '''Returns the value of response code by decoding the byte provided to it'''
        
        if resCode == "00":
            return 'Success'
        elif resCode == "01":
            return 'Command not implemented'
        elif resCode == "02":
            return 'Bad Value- one or more values in the message are invalid'
        elif resCode == "03":
            return 'Command Length Error- command is too long'
        elif resCode == "04":
            return 'Response Length Error- response is too long'
        elif resCode == "05":
            return 'Busy'
        elif resCode == "06":
            return 'Other Error'
  
          
    def getDeviceTypeSGD(self, devType):
        '''Returns the value of device type by decoding the byte provided to it''' 
       
        if devType == "0000":
            return 'Unspecified Type'
   
                
    def getCommodityCode(self, comCode):
        '''Returns the value of commodity by decoding the byte provided to it''' 
        
        if comCode == "00":
            return 'Electricity Consumed, W & W-hr'
        elif comCode == "01":
            return 'Electricity Produced, W & W-hr'
        elif comCode == "02":
            return 'Natural gas, cu-ft/hr & cu-ft'
        elif comCode == "03":
            return 'Water, Gal/hr & Gallons'
        elif comCode == "04":
            return 'Natural gas, cubic meters/hour & cubic meters'
        elif comCode == "05":
            return 'Water, liters/hr & liters'
        else:
            return 'Reserved'
   
            
    def getThermostatMode(self, tMode):
        '''Returns the thermostat mode by decoding the byte provided to it''' 
        
        if tMode == "00":
            return 'Off'
        elif tMode == "01":
            return 'Auto'
        elif tMode == "02":
            return 'Reserved'
        elif tMode == "03":
            return 'Cool'
        elif tMode == "04":
            return 'Heat'
        elif tMode == "05":
            return 'Aux/Emer Heat'
        elif tMode == "06":  
            return 'Reserved'
        elif tMode == "07":  
            return 'Reserved'
  
            
    def getFanMode(self, fMode):
        '''Returns the value of fan mode by decoding the byte provided to it'''
        
        if fMode == "00":
            return 'Auto'
        elif fMode == "01":
            return 'On'
        elif fMode == "02":
            return 'Circulate' 
     
        
    def set_setpoint(self, units, setpoint1, setpoint2):
        '''returns the hex string form of the command to set the setpoints'''
        
        spoint1 = hex(int(setpoint1))[2:]
        spoint2 = hex(int(setpoint2))[2:]
        drAppMsgType = "0802"
        setpointOpcodes = "0303"
        
        payLoad = setpointOpcodes + self.deviceTypeSGD_to_hex('CentralAC-HeatPump') + self.unit_to_hex(units) + \
                    spoint1.rjust(4,'0') + spoint2.rjust(4,'0')
            
        payLoadLen = (hex(int(len(payLoad)/2))[2:]).rjust(4,'0')
        
        msg = drAppMsgType + payLoadLen + payLoad
                
        return msg
    
    
    def set_end_shed_load_cmd(self):
        '''Sends a load shed command'''
        
        return "080100020200"    
        
        
    def set_load_shed(self, duration):
        '''sets the load shed event for the given duration'''
        
        basicDRApp = "0801"
        opcode1 = "01"
        opcode2 = (hex(int(sqrt(duration/2))))[2:].rjust(2,'0')
        msg = basicDRApp + "0002" + opcode1 + opcode2
        return msg
    
    
    def set_critical_peak_demand(self, duration):
        '''sets the critical peak demand event for the given duration'''
        
        basicDRApp = "0801"
        opcode1 = "0A"
        opcode2 = (hex(int(sqrt(duration/2))))[2:].rjust(2,'0')
        msg = basicDRApp + "0002" + opcode1 + opcode2
        return msg
    
    
    def set_grid_emergency(self, duration):
        '''sets the grid emergency event for the given duration'''
        
        basicDRApp = "0801"
        opcode1 = "0B"
        opcode2 = (hex(int(sqrt(duration/2))))[2:].rjust(2,'0')
        msg = basicDRApp + "0002" + opcode1 + opcode2
        return msg
    
    
            
    def set_power_level(self, percentage):
        '''sets the power level to be reduced  to a level between 0 and 100%'''
        
        basicDRApp = "0801"
        opcode1 = "06"
        opcode2 = (hex(int(percentage)))[2:].rjust(2,'0')
        msg = basicDRApp + "0002" + opcode1 + opcode2
        return msg
    
        
    def set_setOffset(self, currentOffset, units):
        '''returns the hex string form of the command to set the temperature offset'''
        
        tempOffset = hex(currentOffset)[2:].rjust(2,'0')
        drAppMsgType = "0802"
        tempOffsetOpcodes = "0302"
        
        payLoad = tempOffsetOpcodes + tempOffset + self.unit_to_hex(units) 
        
        payLoadLen = (hex(int(len(payLoad)/2))[2:]).rjust(4,'0')
        
        msg = drAppMsgType + payLoadLen + payLoad
        
        return msg
    
    
    def set_thermostat_mode(self, systemMode):
        '''returns the hex string form of the command to set the thermostat mode'''
        
        tModeOpcode = "0701"
        tMode = self.thermostat_mode_to_hex(systemMode)
        drAppMsgType = "0802"
        
        payLoad = tModeOpcode + tMode  
        
        payLoadLen = (hex(int(len(payLoad)/2))[2:]).rjust(4,'0')
        
        msg = drAppMsgType + payLoadLen + payLoad
        
        return msg
        
        
    def set_fan_mode(self, fanMode):
        '''returns the hex string form of the command to set the fan mode'''
        
        tModeOpcode = "0702"
        fMode = self.fan_mode_to_hex(fanMode)
        drAppMsgType = "0802"
        
        payLoad = tModeOpcode + fMode  
        
        payLoadLen = (hex(int(len(payLoad)/2))[2:]).rjust(4,'0')
        
        msg = drAppMsgType + payLoadLen + payLoad
        
        return msg
    
    
    def unit_to_hex(self, unit):
        
        if unit == 'F':
            return "00"
        elif unit =='C':
            return "01"
        
        
    def deviceTypeSGD_to_hex(self, deviceType):
        
        if deviceType == 'Unspecified Type':
            return "0000"
        elif deviceType == 'CentralAC-HeatPump':
            return "0004"
        
        
    def thermostat_mode_to_hex(self, systemMode):
        
        if systemMode == 'Off':
            return "00"
        elif systemMode == 'Auto':
            return "01"
        elif systemMode == 'Reserved':
            return "02"
        elif systemMode == 'Cool':
            return "03"
        elif systemMode == 'Heat':
            return "04"
        elif systemMode == 'Aux/Emer Heat':
            return "05"
        elif systemMode == 'Reserved':
            return "06"
        elif systemMode == 'Reserved':
            return "07"
        
        
    def fan_mode_to_hex(self, fanMode):
        
        if fanMode == 'Auto':
            return "00"
        elif fanMode == 'On':
            return "01"
        elif fanode == 'Circulate':
            return "02"      
        
    