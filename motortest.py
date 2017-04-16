import RPi.GPIO as GPIO
from time import sleep
from pololu_drv8835_rpi import motors, MAX_SPEED

motors.motor1.setSpeed(50)
motors.motor2.setSpeed(50)