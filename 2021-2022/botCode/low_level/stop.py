
from GPIOhelpers import *
from pins import *
setGPIO()
analogMode(pins.motor_speed_r, 0)
analogMode(pins.motor_speed_l, 0)

analogWrite(pins.motor_speed_r,0)
analogWrite(pins.motor_speed_l,0)
            
            #GPIO.setup(10, OUTPUT)
            #pwm = GPIO.PWM(10, 490)
            #pwm.start(90)
            #sleep(3)
