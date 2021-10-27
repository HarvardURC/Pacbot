#to be run on a raspberry pi (which has raspbian, which in turn has RPi module installed on it)

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#pins: 
#"motor_speed_r" : 11,
#"motor_direction_r" : 9
digitalWrite(9, 1)
11.ChangeDutyCycle(50)
