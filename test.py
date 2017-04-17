import RPi.GPIO as GPIO
import smbus
import time

left_pulses = 0
right_pulses = 0

address = 0x29
bus = smbus.SMBus(1)

class Test_Encoders():

    def __init__(self):
        
        GPIO.setmode(GPIO.BCM)
        #Setup each hall effect pin for interrupts
        GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        print ("Encoders Ready")
        
        GPIO.add_event_detect(18, GPIO.FALLING, callback=self.add_right_pulse)
        GPIO.add_event_detect(24, GPIO.FALLING, callback=self.add_left_pulse)

        while 1:
            pass

    # Callback function for Hall Sensor interrupts
    def add_left_pulse(self, channel):
        global left_pulses
        left_pulses += 1
##        print ("\nLeft Pulses: ")
##        print (left_pulses)
    def add_right_pulse(self, channel):
        global right_pulses
        right_pulses += 1
##        print ("\nRight Pulses: ")
##        print (right_pulses)

class Test_Motors():

    def __init__(self):

        GPIO.setmode(GPIO.BCM)
        # output for left motor
        GPIO.setup(26, GPIO.OUT)
        GPIO.setup(19, GPIO.OUT)
        # output for right motor
        GPIO.setup(13, GPIO.OUT)
        GPIO.setup(6, GPIO.OUT)
        print ("Motors Ready")

if __name__ == '__main__':
    try:
        Test_Encoders()
        Test_Motors()

    except KeyboardInterrupt:
        print ("\nLeft Motor Pulses: ")
        print (left_pulses)
        print ("\nRight Motor Pulses: ")
        print (right_pulses)
        GPIO.cleanup()

