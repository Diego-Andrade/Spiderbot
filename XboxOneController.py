# Author: Diego Andrade
# Purpose: Handle event codes, register listeners, and trigger
#          listners to new events recieved

import sys
from evdev import InputDevice, categorize, ecodes

class XboxOneController:

    # Class to facilitate storing listners for later callback
    class XboxEventListner:
        event = None
        listner = None
        callBack = None
        
        def __init__(self, event, listner, callBack):
            self.event = event
            self.listner = listner
            self.callBack = callBack
    
    # Controller mapping
    map = {
        "A":      304,
        "B":      305,
        "X":      307,
        "Y":      308,
        "LB":     310,
        "RB":     311,
        "L3":     317,
        "R3":     318,
        "Select": 314,
        "Start":  315,
        "LT":    "ABS_Z",
        "RT":    "ABS_RZ",
        "LX":    "ABS_X",
        "LY":    "ABS_Y",
        "RX":    "ABS_RX",
        "RY":    "ABS_RY"
    }
        
    def __init__(self, deviceLocation, deadzoneAxis=0.0, deadzoneTriggers=0.0):
        try:
            # List of listners, populated once they register
            self.listners = []

            # For reconnecting later
            self.deviceLocation = deviceLocation

            # Deadzone defining
            self.deadzoneAxis = deadzoneAxis
            self.deadzoneTriggers = deadzoneTriggers

            # The controller
            self.gamepad = InputDevice(deviceLocation)
            self.controllerConnected = True
        except OSError:
            print("Controller not found at location '{}'".format(deviceLocation))
            print("Check if controller connected correctly")
            self.controllerConnected = False;
            #sys.exit()
    def registerListner(self, event, listner, callBack):
        if event in self.map:
            newListner = self.XboxEventListner(self.map[event], listner, callBack)
            self.listners.append(newListner)
        else:
            raise Exception('Event requested not supported', event)
        
    def handleEvent(self):
        try:
            # Handle reconnecting
            if (not self.controllerConnected):
                try:
                    self.gamepad = InputDevice(self.deviceLocation)
                    self.controllerConnected = True
                    print("Controller reconnected!")
                except OSError:
                    return

            # Get event, throws IOError if controller disconnected
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
        except IOError:
            print("Cannot get event from controller. Was it disconnected?")
            self.controllerConnected = False;
    def scaleAxis(self, axis, value):
        if axis == self.map["LT"] or axis == self.map["RT"]:
            # Range for LT and RT is 0 - 1023
            percentageValue = value / 1023.0
            
            if (abs(percentageValue) < self.deadzoneTriggers):
                percentageValue = 0.0
            
            return percentageValue
        else:
            percentageValue = value / 32768.0

            if (abs(percentageValue) < self.deadzoneAxis):
                percentageValue = 0.0
                
            return percentageValue
            
    
    
