import numpy as np
# Grid enums
I = 1
o = 2
e = 3
O = 4
n = 5

# Threshold values for yellow dots
# Order is H S V
lower_yellow = np.array([23,33,206])
upper_yellow = np.array([38,190,255])

lower_green = np.array([40,22,129])
upper_green = np.array([70,196,255])
