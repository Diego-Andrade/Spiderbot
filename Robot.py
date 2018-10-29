# Author: Diego Andrade
# Purpose: Using an xbox controller to control motors set up
#          in a tank drive configuration

import RPi.GPIO as GPIO
from XboxOneController import XboxOneController
from VEXMotorController29 import VEXMotorController29

# Wiring mapping
motorRightPort1 = 18
motorRightPort2 = 19

motorLeftPort1 = 17
motorLeftPort2 = 16

arm1 = 23

class Robot:
    
    def __init__(self):
        # Set up controller
        self.controller = XboxOneController('/dev/input/event0')
        
        # Set up listners
        self.controller.registerListner("A", self, self.handleA) 
        self.controller.registerListner("LY", self, self.handleLY)
        self.controller.registerListner("RY", self, self.handleRY)
        
        # Set up drive motors
        self.motorRight1 = VEXMotorController29(motorRightPort1)
        self.motorRight2 = VEXMotorController29(motorRightPort2)
        
        self.motorLeft1 = VEXMotorController29(motorLeftPort1)
        self.motorLeft2 = VEXMotorController29(motorLeftPort2)

        # Set up arms
        self.arm1 = VEXMotorController29(arm1)




    def loop(self):
        self.controller.handleEvent()

    ########## Call back methods ############
    # When event is picked up by controller module, it will call one of
    # these methods to handle the event

    # Called when a new A value is recieved
    def handleA(self, value):
        print("A pressed: {}".format(value))
        if (value == 1):
            self.arm1.set(1)
        else:
            self.arm1.set(-1)    
        
    # Called when a new LY value is recieved
    def handleLY(self, value):
        self.motorLeft1.set(value * -1)
        self.motorLeft2.set(value * -1)
     
    # This gets called when right stick is moved on xbox controller
    def handleRY(self, value):
        self.motorRight1.set(value * -1)
        self.motorRight2.set(value * -1)
        

# ********************** MAIN LOOP *********************

if __name__ == "__main__":
    try:
        # Disabling gpio warnings
        GPIO.setwarnings(False)
        
        robot = Robot()

        # Display gamepad to verify correct controller
        print(robot.controller.gamepad)
        
        while True:
            robot.loop()    
            
    except KeyboardInterrupt:
        GPIO.cleanup()
