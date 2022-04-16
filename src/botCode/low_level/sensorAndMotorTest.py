from .motors import Motors
from time import sleep

def test_sensor_response():
    motors = Motors()
    motors.straight()

    while 1:
        sleep(0.01)
        motors.teensy_sensors.print_orig_values()

test_sensor_response()
    
