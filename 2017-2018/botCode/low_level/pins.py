from types import SimpleNamespace

'''pins = SimpleNamespace(**{
    "led" : 1,
    "motor_power_r": 26,
    "motor_power_l" : 13,
    "motor_direction_l" : 19,
    "motor_direction_r" : 6,
    "tof_front" : 0;
    "tof_left" : 0,
    "tof_left_diag" : 0,
    "tof_front" : 0,
    "tof_right_diag" : 0,
    "tof_right" : 0})
'''
pins = SimpleNamespace(**{"led" : 1, 
    "tof_left" : 15, "tof_right" : 18, 
    "encoder_pin_l1" : 17, 
    "encoder_pin_l2" : 27, 
    "motor_power_l" : 13,
    "motor_direction_l" : 19})
