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
    "tof_front" : 27,
    "tof_fleft" : 18,
    "tof_fright" : 23,
    "tof_rear" : 13,
    "tof_rleft" : 6,
    "tof_rright" :26,
    "encoder_pin_l1" : 4, 
    "encoder_pin_l2" : 14,
    "encoder_pin_r1" : 15, 
    "encoder_pin_r2" : 17, 
    "motor_speed_l" : 10,
    "motor_direction_l" : 24,
    "motor_speed_r" : 11,
    "motor_direction_r" : 9})
