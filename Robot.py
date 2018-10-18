# Author: Diego Andrade
# Purpose: Using an xbox controller to control motors set up
#          in a tank drive configuration

import RPi.GPIO as GPIO
from XboxOneController import XboxOneController
from VEXMotorController29 import VEXMotorController29


# Wiring mapping
motor1Port = 16
motor2Port = 20

class Robot:
    # Defining objects
    controller = None
    motor1 = None
    motor2 = None
    
    def __init__(self):
        # Set up controller
        self.controller = XboxOneController('/dev/input/event0')
        
        # Set up listners
        self.controller.registerListner("A", self, self.handleA) 
        self.controller.registerListner("LY", self, self.handleLY)
        self.controller.registerListner("RY", self, self.handleRY)
        
        # Set up motors
        self.motor1 = VEXMotorController29(motor1Port)
        self.motor2 = VEXMotorController29(motor2Port)


    def loop(self):
        self.controller.handleEvent()

    ########## Call back methods ############
    # When event is picked up by controller module, it will call one of
    # these methods to handle the event

    # Called when a new A value is recieved
    def handleA(self, value):
        print("CallBack for A: ", value)
        
    # Called when a new LY value is recieved
    def handleLY(self, value):
        self.motor1.set(value * -1)
        
    def handleRY(self, value):
        self.motor2.set(value * -1)
        

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
