# Author: Diego Andrade
# Purpose: Using an xbox controller to control motors set up
#          in a tank drive configuration

import RPi.GPIO as GPIO
from XboxOneController import XboxOneController
from VEXMotorController29 import VEXMotorController29

# Wiring mapping

# Breakout layout
v7port1 = 2
v7port2 = 3
v7port3 = 4
v7port4 = 14
v7port5 = 19
v7port6 = 16
v7port7 = 20
v7port8 = 26

v5port1 = 15 
v5port2 = 18
v5port3 = 23
v5port4 = 24
v5port5 = 25
v5port6 = 8
v5port7 = 7
v5port8 = 12

motorRightPort1 = v7port1
motorRightPort2 = v7port2

motorLeftPort1 = v7port3
motorLeftPort2 = v7port4

armLeft1 = v5port1
armLeft2 = v5port2
armLeft3 = v5port3
armLeft4 = v5port4
armRight1 = v5port5
armRight2 = v5port6
armRight3 = v5port7
armRight4 = v5port8

class Robot:
    
    def __init__(self):
    # Set up controller
        self.controller = XboxOneController('/dev/input/event0')
        
    # Set up listners
        # Drive   
        self.controller.registerListner("LY", self, self.handleLY)
        self.controller.registerListner("RY", self, self.handleRY)

        # Arm1
        self.controller.registerListner("A", self, self.handleA) 
        self.controller.registerListner("RT", self, self.handleRT)
        self.controller.registerListner("LT", self, self.handleLT)

        
    # Set up drive motors
        self.motorRight1 = VEXMotorController29(motorRightPort1)
        self.motorRight2 = VEXMotorController29(motorRightPort2)
        self.motorLeft1 = VEXMotorController29(motorLeftPort1)
        self.motorLeft2 = VEXMotorController29(motorLeftPort2)

    # Set up arms
        self.armLeft1 = VEXMotorController29(armLeft1, -1.0, 0.5)
        self.armLeft2 = VEXMotorController29(armLeft2, -1.0, 0.5)
        self.armLeft3 = VEXMotorController29(armLeft3, -1.0, 0.5)
        self.armLeft4 = VEXMotorController29(armLeft4, -1.0, 0.5)
        self.armRight1 = VEXMotorController29(armRight1, -1.0, 0.5)
        self.armRight2 = VEXMotorController29(armRight2, -1.0, 0.5)
        self.armRight3 = VEXMotorController29(armRight3, -1.0, 0.5)
        self.armRight4 = VEXMotorController29(armRight4, -1.0, 0.5)


    def loop(self):
        self.controller.handleEvent()

    ########## Call back methods ############
    # When event is picked up by controller module, it will call one of
    # these methods to handle the event

    def handleA(self, value):\
        # Called when a new 'A' value is recieved
        if (value == 1):
            self.armLeft1.set(1)
            self.armLeft2.set(1)
            self.armLeft3.set(1)
            self.armLeft4.set(1)
            self.armRight1.set(1)
            self.armRight2.set(1)
            self.armRight3.set(1)
            self.armRight4.set(1)
        else:
            self.armLeft1.set(-1)
            self.armLeft2.set(-1)
            self.armLeft3.set(-1)
            self.armLeft4.set(-1)
            self.armRight1.set(-1)
            self.armRight2.set(-1)
            self.armRight3.set(-1)
            self.armRight4.set(-1)   
        
    def handleLY(self, value):
        # Called when a new LY value is recieved
        self.motorLeft1.set(value * -1)
        self.motorLeft2.set(value * -1)
     
    def handleRY(self, value):\
        # This gets called when right stick is moved on xbox controller
        self.motorRight1.set(value * -1)
        self.motorRight2.set(value * -1)
        
    def handleRT(self, value):
        pass
        # Move arm1 up
        #self.arm1.set(value)

    def handleLT(self, value):
        pass
        # Multiply by -1 because LT moves arm1 down
        #self.arm1.set(value * -1)

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
