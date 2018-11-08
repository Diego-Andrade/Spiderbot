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
    
    def __init__(self, port, lowerMS, centerMS, upperMS):
	self.lowerMS = lowerMS
	self.centerMS = centerMS
	self.upperMS = upperMS
	
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(port, GPIO.OUT)
        self.motor = GPIO.PWM(port, 50)
        self.motor.start(0)
        self.set(0)
        
    def set(self, value):
        if (value < 0):
             targetMS = (self.centerMS - self.lowerMS) * value + self.centerMS
        else:
             targetMS = (self.upperMS - self.centerMS) * value + self.centerMS               
             
        pwmOut = targetMS * 5
        self.motor.ChangeDutyCycle(pwmOut)

        #print(targetMS)
