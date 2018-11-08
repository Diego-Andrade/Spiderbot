# Author: Diego Andrade
# Purpose: Handle event codes, register listeners, and trigger
#          listners to events
# Date: 11/7/18

from evdev import InputDevice, categorize, ecodes

class PS4Controller:
    class PS4EventListner:
        event = None
        listner = None
        callBack = None
        
        def __init__(self, event, listner, callBack):
            self.event = event
            self.listner = listner
            self.callBack = callBack
    
    # Controller mapping
    map = {
        "X":        304,
        "O":        305,
        "S":        308,
        "T":        307,
        "L1":       310,
        "R1":       311,
        "L2":       312,
        "R2":       313,
        "L3":       317,
        "R3":       318,
        "Share":    314,
        "Options":  315,
        "LX":       "ABS_X",
        "LY":        "ABS_Y",
        "RX":       "ABS_RX",
        "RY":       "ABS_RY",
        "L2Axis":   "ABS_Z",
        "R2Axis":   "ABS_RZ"
    }
    
    # Gamepad object to read events
    gamepad = None
    
    # List of listners
    listners = []
    
    # Deadzone
    deadzoneAxis = 0.0
    deadzoneTriggers = 0.0
    
    def __init__(self, deviceLocation):
        self.gamepad = InputDevice(deviceLocation)
        
    def registerListner(self, event, listner, callBack):
        if event in self.map:
            newListner = self.XboxEventListner(self.map[event], listner, callBack)
            self.listners.append(newListner)
        else:
            raise Exception('Event requested not supported', event)
        
    def handleEvent(self):
        event = self.gamepad.read_one()
        
        if event == None:
            return
        
        for listner in self.listners:
            if event.type == ecodes.EV_KEY:
                if listner.event == event.code:
                    listner.callBack(event.value)
            elif event.type == ecodes.EV_ABS:
                absevent = categorize(event)
                if listner.event == ecodes.bytype[absevent.event.type][absevent.event.code]:
                    listner.callBack(self.scaleAxis(listner.event, absevent.event.value))
                
                
    def scaleAxis(self, axis, value):
        percentageValue = (value - 127.5) / 127.5

        if (abs(percentageValue) < self.deadzoneAxis):
                percentageValue = 0.0

        return percentageValue
        
##        if axis == self.map["LT"] or axis == self.map["RT"]:
##            # Range for LT and RT is 0 - 1023
##            percentageValue = value / 1023.0
##            
##            if (abs(percentageValue) < self.deadzoneTriggers):
##                percentageValue = 0.0
##            
##            return percentageValue
##        else:
##            percentageValue = value / 32768.0
##
##            if (abs(percentageValue) < self.deadzoneAxis):
##                percentageValue = 0.0
##                
##            return percentageValue
            
    
    
