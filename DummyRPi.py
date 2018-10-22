class GPIO:
    BOARD = 0
    BCM = 1
    OUT = 0
    IN = 1

    @classmethod
    def setmode(cls, mode):
        print("Setting mode", mode)

    @classmethod
    def setup(cls, port, mode):
        if (mode == cls.OUT):
            print("Setting port {} as OUT".format(port))
        elif (mode == cls.IN):
            print("Setting port {} as IN".format(port))
        else:
            print("Error mode not recognised")

    @classmethod
    def PWM(cls, port, freq):
        print("PWM on port {} with frequency of {} hz created".format(port, freq))
        newInst = GPIO()
        newInst.port = port
        newInst.freq = freq
        return newInst

    def start(self, dutycycle):
        print("Starting pwm on port {} with frequency of {} hz and duty cycle of {}".format(self.port, self.freq, dutycycle))
        self.dutycycle = dutycycle

    def ChangeDutyCycle(self, dutycycle):
        print ("Change duty cycle for port {} from {} to {}".format(self.port, self.dutycycle, dutycycle))


    @classmethod
    def cleanup(cls):
        print("Pins cleaned up") 
    