# Author: Diego Andrade
# Purpose: Using an xbox controller to control motors set up
#          in a tank drive configuration

import RPi.GPIO as GPIO
import time
from XboxOneController import XboxOneController
from PS4Controller import PS4Controller
#from VEXMotorController29 import VEXMotorController29

from ServoArm import ServoArm

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

motorRightPort1 = 6
motorRightPort2 = 7

motorLeftPort1 = 4
motorLeftPort2 = 5

armLeft1 = 2
armLeft2 = 3
armLeft3 = 13
armLeft4 = 12
armRight1 = 0
armRight2 = 1
armRight3 = 15
armRight4 = 14

class Robot:

    # Map of position to
    walkPos = {
        armLeft1: 1,
        armLeft2: -1,
        armLeft3: 1,
        armLeft4: -1,
        armRight1: 1,
        armRight2: -1,
        armRight3: 1,
        armRight4: -1,
    }

    walkDir = {
        armLeft1: 1,
        armLeft2: -1,
        armLeft3: 1,
        armLeft4: -1,
        armRight1: 1,
        armRight2: -1,
        armRight3: 1,
        armRight4: -1
    }

    currentWalk = 0
    walkTickAmount = 0.02
    walkingLeft = False
    walkingRight = False

    walkManual = False;

    def __init__(self):
    # Set up controller
        self.controller = XboxOneController('/dev/input/event0', deadzoneAxis = 0.18)
        #self.controller = PS4Controller('/dev/input/event2', deadzoneAxis = 0.18)

    # Set up listners
        # Drive
        self.controller.registerListner("LY", self, self.handleLY)
        self.controller.registerListner("RY", self, self.handleRY)

        # Arm1
        self.controller.registerListner("A", self, self.handleX)
        self.controller.registerListner("Y", self, self.handleT)
        self.controller.registerListner("X", self, self.handleS)
        self.controller.registerListner("B", self, self.handleO)

        self.controller.registerListner("LT", self, self.handleL2Axis)
        self.controller.registerListner("RT", self, self.handleR2Axis)



    # Set up drive motors
        self.motorRight1 = ServoArm(motorRightPort1, 1000, 2000)
        self.motorRight2 = ServoArm(motorRightPort2, 1000, 2000)
        self.motorLeft1 = ServoArm(motorLeftPort1, 1000,2000)
        self.motorLeft2 = ServoArm(motorLeftPort2, 1000, 2000)

        self.motorRight1.set(0)
        self.motorRight2.set(0)
        self.motorLeft1.set(0)
        self.motorLeft2.set(0)

    # Set up arms
        self.armLeft1 = ServoArm(armLeft1, 1450, 1000) #inverted
        self.armLeft2 = ServoArm(armLeft2, 1300, 1700)
        self.armLeft3 = ServoArm(armLeft3, 1300, 1000) #inverted
        self.armLeft4 = ServoArm(armLeft4, 1300, 1800)

        self.armRight1 = ServoArm(armRight1, 1300, 1800)
        self.armRight2 = ServoArm(armRight2, 1400, 1000) #inverted
        self.armRight3 = ServoArm(armRight3, 1300, 1780)
        self.armRight4 = ServoArm(armRight4, 1400, 1000) #inverted

    def loop(self):
        self.controller.handleEvent()
        self.walkTick()

        if (not self.walkManual):
            if (self.walkingLeft):
                self.walkLeft()

            if (self.walkingRight):
                self.walkRight()

        #Slow down to resonable speed
        time.sleep(0.0001)


    ########## Call back methods ############
    # When event is picked up by controller module, it will call one of
    # these methods to handle the event

    def handleX(self, value):
        # Called when a new 'X' value is recieved
        if (value == 1):
            self.armLeft1.set(1.0)
            self.armLeft2.set(1.0)
            self.armLeft3.set(1.0)
            self.armLeft4.set(1.0)

            self.armRight1.set(1.0)
            self.armRight2.set(1.0)
            self.armRight3.set(1.0)
            self.armRight4.set(1.0)
        else:
            self.armLeft1.set(-1.0)
            self.armLeft2.set(-1.0)
            self.armLeft3.set(-1.0)
            self.armLeft4.set(-1.0)

            self.armRight1.set(-1.0)
            self.armRight2.set(-1.0)
            self.armRight3.set(-1.0)
            self.armRight4.set(-1.0)

    def handleS(self, value):
        # Called when a new 'S' value is recieved
        if (value == 1):
            self.armLeft1.set(1.0)
            self.armLeft2.set(1.0)
            self.armLeft3.set(1.0)
            self.armLeft4.set(1.0)
        else:
            self.armLeft1.set(-1.0)
            self.armLeft2.set(-1.0)
            self.armLeft3.set(-1.0)
            self.armLeft4.set(-1.0)

    def handleO(self, value):
        # Called when a new 'O' value is recieved
        if (value == 1):
            self.armRight1.set(1.0)
            self.armRight2.set(1.0)
            self.armRight3.set(1.0)
            self.armRight4.set(1.0)
        else:
            self.armRight1.set(-1.0)
            self.armRight2.set(-1.0)
            self.armRight3.set(-1.0)
            self.armRight4.set(-1.0)

    def handleT(self, value):
        if (value == 0):
            self.walkManual = not self.walkManual
            time.sleep(0.01)

    def handleL2Axis(self, value):
        if (self.walkManual):
            self.armLeft1.set(value)
            self.armLeft2.set(value)
            self.armLeft3.set(value)
            self.armLeft4.set(value)

    def handleR2Axis(self, value):
        if (self.walkManual):
            self.armRight1.set(value)
            self.armRight2.set(value)
            self.armRight3.set(value)
            self.armRight4.set(value)
    def handleLY(self, value):
        # Called when a new LY value is recieved
        self.motorLeft1.set(value * -1)
        self.motorLeft2.set(value * -1)
        if (value != 0):
            self.walkingLeft = True;
        else:
            self.walkingLeft = False;

    def handleRY(self, value):
        # This gets called when right stick is moved on xbox controller
        self.motorRight1.set(value)
        self.motorRight2.set(value)
        if (value != 0):
            self.walkingRight = True;
        else:
            self.walkingRight = False;

    def walkTick(self):
        for key, value in self.walkPos.items():
            # End cases
            if (value <= -1 or value >= 1):
                self.walkDir[key] *= -1

            self.walkPos[key] = value + self.walkTickAmount * self.walkDir[key]


    def walk(self):
        self.armLeft1.set(self.walkPos[armLeft1])
        self.armLeft2.set(self.walkPos[armLeft2])
        self.armLeft3.set(self.walkPos[armLeft3])
        self.armLeft4.set(self.walkPos[armLeft4])

        self.armRight1.set(self.walkPos[armRight1])
        self.armRight2.set(self.walkPos[armRight2])
        self.armRight3.set(self.walkPos[armRight3])
        self.armRight4.set(self.walkPos[armRight4])

    def walkLeft(self):
        self.armLeft1.set(self.walkPos[armLeft1])
        self.armLeft2.set(self.walkPos[armLeft2])
        self.armLeft3.set(self.walkPos[armLeft3])
        self.armLeft4.set(self.walkPos[armLeft4])

    def walkRight(self):
        self.armRight1.set(self.walkPos[armRight1])
        self.armRight2.set(self.walkPos[armRight2])
        self.armRight3.set(self.walkPos[armRight3])
        self.armRight4.set(self.walkPos[armRight4])


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
