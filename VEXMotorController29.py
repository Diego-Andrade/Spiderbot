# Author: Diego Andrade
# Purpose: Motor class handling conversions and outputs
# Notes: Only from vex 393 motor controlled with a motor controller 29
#        Pwm frequency of 50 hz with duty cycle being calculated to give
#        1ms - 2ms pulses for motor controller 29
 
import platform
 
if (platform.system() == 'Windows'):
     from DummyRPi import GPIO
else:
    import RPi.GPIO as GPIO

class VEXMotorController29:
    
    def __init__(self, port, lowerLimit = -1.0, upperLimit = 1.0):
	self.lowerLimit = lowerLimit
	self.upperLimit = upperLimit
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(port, GPIO.OUT)
        self.motor = GPIO.PWM(port, 50)
        self.motor.start(0)
        self.set(0)
        
    def set(self, value):
        if (value > self.upperLimit):
	    self.set(self.upperLimit)
	    return
	elif (value < self.lowerLimit):
            self.set(self.lowerLimit)
            return
        # motor controller 29 requires 1ms - 2ms signal
        # 1.5 is off, so from center +- 0.5ms
        # 0.5 * percentage setting + off pos
        targetMS = 0.5 * value + 1.5
        pwmOut = targetMS * 5
        
        self.motor.ChangeDutyCycle(pwmOut)
