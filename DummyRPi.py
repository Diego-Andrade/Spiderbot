# Author: Diego Andrade
# Purpose: A dummy class created inorder to allowing running of  code
#          that depends on the raspberrypi's RPi.GPIO class that is not
#          availible outside of pi

class GPIO:
    # Board mode const
    BOARD = 'BOARD'
    BCM = 'BCM'

    # Pin mode setup
    OUT = 'OUT'
    IN = 'IN'

    # Pin out values
    HIGH = 'HIGH'
    LOW = 'LOW'

    # Dict to keep track of pin states
    portStates = dict()

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
    def output(cls, port, value):
        if (value != cls.HIGH or value != cls.LOW):
            print("Cannot set port {} to {}. Invalid value".format(port, value))
            return
            
        print("Port {}: {}".format(port, value))
        cls.portStates[port] = value

    @classmethod
    def input(cls, port):
        return cls.portStates[port]
    

    @classmethod
    def cleanup(cls):
        print("Pins cleaned up") 

    class PWM:    
        def __init__(self, port, freq):
            print("PWM(port={}, freq={}) created".format(port, freq))
            self.port = port
            self.freq = freq

        def start(self, dutycycle):
            print("Starting pwm: port {} {}hz {}%".format(self.port, self.freq, dutycycle))
            self.dutycycle = dutycycle

        def ChangeDutyCycle(self, dutycycle):
            print ("Port {} duty cycle changed: {} -> {}".format(self.port, self.dutycycle, dutycycle))
            self.dutycycle = dutycycle

