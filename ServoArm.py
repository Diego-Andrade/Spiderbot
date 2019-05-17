# Servo arm implementation, taking care of all arm controll logic

from adafruit_servokit import ServoKit

class ServoArm:

    kit = ServoKit(channels=16)

    def __init__(self, servo, lower_limit = 0, upper_limit = 45):
        # servo - the servo object or port
        self.servo = ServoArm.kit.servo[servo]
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit

        #setup servo
        self.servo.set_pulse_width_range(lower_limit, upper_limit)

    def set(self, val):
        # val range is [0, 1]
        self.servo.angle = 180 * (val+1)/2

    def get(self):
        return self.servo.angle
