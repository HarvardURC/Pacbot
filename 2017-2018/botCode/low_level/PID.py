""" PID library
Converted from arduino library: http://playground.arduino.cc/Code/PIDLibrary 
Explanation at: http://brettbeauregard.com/blog/2011/04/improving-the-beginners-pid-introduction/
"""
AUTOMATIC = 1
MANUAL = 0
DIRECT = 1
REVERSE = 0
class PID:
    # constants
    AUTOMATIC = 1
    MANUAL = 0
    DIRECT = 1
    REVERSE = 0

    def __init__(self, inp, setpoint, kp, ki, kd, controller_direction, timer):
        self._input = inp
        self._setpoint = setpoint
        self._timer = timer()
        self._in_auto = False
        self._output = 0
        self._controller_direction = controller_direction
        self._last_input = 0

        # default output limits
        self.set_output_limits(0, 255)

        # default controller sample time is 0.1 seconds
        self._sample_time = 100

        self.set_controller_direction(self._controller_direction)

        self.set_tunings(kp, ki, kd)

        self._last_time = self.millis() - self._sample_time

    def compute(self, my_input, my_setpoint):
        """ compute is called evertime loop excutes.
        It decides for itself whether new output needs to be computed.
        Returns True when output is computed and false otherwise.
        """ 
        if not self._in_auto:
            return False

        self._input = my_input
        self._setpoint = my_setpoint

        now = self.millis()
        time_change = now - self._last_time

        if time_change < self._sample_time:
            return False

        # compute all working error variables
        error = self._setpoint - self._input
        self._I_term += self._ki * error
        
    
        if self._I_term > self._out_max:
            self._I_term = self._out_max
        elif self._I_term < self._out_min:
            self._I_term = self._out_min

        d_input = self._input - self._last_input

        # compute PID output
        self._I_term = 0
        output = self._kp * error + self._I_term - self._kd * d_input

        if output > self._out_max:
            output = self._out_max
        elif output < self._out_min:
            output = self._out_min

        self._output = output

        # update relevant variables
        self._last_input = self._input
        self._last_time = now

        return True

    def output(self):
        return self._output

    def set_tunings(self, kp, ki, kd):
        """ Allows the controllers dynamic performance to be adjusted."""
        if kp < 0 or ki < 0 or kd < 0:
            return

        self._disp_kp = kp
        self._disp_ki = ki
        self._disp_kd = kd

        sample_time_in_sec = self._sample_time / 1000

        self._kp = kp
        self._ki = ki * sample_time_in_sec
        self._kd = kd / sample_time_in_sec

        if self._controller_direction == REVERSE:
            self._kp = - self._kp
            self._ki = - self._ki
            self._kd = - self._kd

    def set_sample_time(self, new_sample_time):
        """ sets the period, in milliseconds, at which the calculation is performed. """
        if new_sample_time <= 0:
            return

        ratio = new_sample_time / self._sample_time
        self._ki *= ratio
        self._kd /= ratio
        self._sample_time = new_sample_time

    def set_output_limits(self, min, max):
        if min >= max:
            return

        self._out_min = min
        self._out_max = max

        if self._in_auto:
            if self._output > self._out_max:
                self._output = self._out_max
            elif self._output < self._out_min:
                self._output = self._out_min

            if self._I_term > self._out_max:
                self._I_term = self._out_max
            elif self._I_term < self._out_min:
                self._I_term = self._out_min

    def set_mode(self, mode):
        """ Allows the controller mode to be set to MANUAL or AUTOMATIC.
        When mode if changed from manual to auto, the controller is automatically (re)initialized.
        """
        new_auto = (mode == AUTOMATIC)

        if  new_auto and not self._in_auto:
            self._intialize()

        self._in_auto = new_auto

    def _intialize(self):
        """ Handles mode change from manual to auto. """
        self._I_term = 0
        self._last_input = self._input

        if self._I_term > self._out_max:
            self._I_term = self._out_max
        elif self._I_term < self._out_min:
            self._I_term = self._out_min

    def set_controller_direction(self, direction):
        """ DIRECT: +output -> +input
        REVERSE: +output -> -input
        """
        if self._in_auto and direction != self._controller_direction:
            self._kp = - self._kp
            self._ki = - self._ki
            self._kd = - self._kd

        self._controller_direction = direction

    def get_kp(self):
        return self._disp_kp

    def get_ki(self):
        return self._disp_ki

    def get_kd(self):
        return self._disp_kd

    def get_mode(self):
        if self._in_auto:
            return AUTOMATIC
        else:
            return MANUAL

    def get_direction(self):
        return self._controller_direction

    def millis(self):
        return self._timer.millis()

        


