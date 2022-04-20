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
pins = SimpleNamespace(**{ 
    "tof_front" : 21,
    "tof_fleft" : 23,
    "tof_fright" : 20,
    "tof_rear" : 22,
    "tof_rleft" : 4,
    "tof_rright" : 24,
    "motor_speed_l" : 18,
    "motor_direction_l" : 19,
    "motor_speed_r" : 12,
    "motor_direction_r" : 6})
