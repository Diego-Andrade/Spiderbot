# Author: Diego Andrade
# Purpose: A dummy class created inorder to allowing running of  code
#          that depends on the raspberrypi's RPi.GPIO class that is not
#          availible outside of pi

class GPIO:
    BOARD = 'BOARD'
    BCM = 'BCM'
    OUT = 'OUT'
    IN = 'IN'

    @classmethod
    def setmode(cls, mode):
        print("Setting mode", mode)

    @classmethod
    def setup(cls, port, mode):
        if (mode == cls.OUT or mode == cls.IN):
            print("Setting port {} as {}".format(port, mode))
        else:
            print("Error mode not recognised")

    @classmethod
    def cleanup(cls):
        print("Pins cleaned up") 

    class PWM:    
        def __init__(self, port, freq):
            print("PWM on port {} with frequency of {} hz created".format(port, freq))
            self.port = port
            self.freq = freq

        def start(self, dutycycle):
            print("Starting pwm on port {} with frequency of {} hz and duty cycle of {}".format(self.port, self.freq, dutycycle))
            self.dutycycle = dutycycle

        def ChangeDutyCycle(self, dutycycle):
            print ("Change duty cycle for port {} from {} to {}".format(self.port, self.dutycycle, dutycycle))
            self.dutycycle = dutycycle

