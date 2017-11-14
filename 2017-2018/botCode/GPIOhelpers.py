import RPi.GPIO as GPIO 

HIGH = GPIO.HIGH
LOW = GPIO.LOW
OUTPUT = GPIO.OUT
INPUT = GPIO.IN
INPUT_PULLUP = GPIO.PUD_UP
CHANGE = GPIO.BOTH
RISING = GPIO.RISING
FALLING = GPIO.FALLING

pwmPins = {}

def setGPIO():
	return GPIO.setmode(GPIO.BCM)

def digitalMode(pin, mode):
	if mode == INPUT_PULLUP:
		return GPIO.setup(pin, INPUT, pull_up_down = INPUT_PULLUP)
	else:
		return GPIO.setup(pin, mode)

def analogMode(pin, duty_cycle):
	GPIO.setup(pin, OUTPUT)
	pwm = GPIO.PWM(pin, 490)
	pwm.start(duty_cycle)
	return pwmPins.update({pin:pwm})

def analogWrite(pin, duty_cycle):
	return pwmPins[pin].ChangeDutyCycle(duty_cycle)

def digitalWrite(pin, value):
	return GPIO.output(pin, value)

def digitalRead(pin):
	return GPIO.input(pin)

def clearAllPins():
	return GPIO.cleanup()

def attachInterrupt(pin, my_callback, event):
	return GPIO.add_event_detect(pin, event, callback=my_callback)


