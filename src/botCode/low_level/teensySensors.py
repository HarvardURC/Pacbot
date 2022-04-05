#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
import threading
from time import sleep

class SensorsV2():
    def __init__(self):
        # Instance variables for current sensor values
        self.heading = None
        self.left_encoder = None
        self.right_encoder = None

        # Set up communication with teensy
        self.serial_port = serial.Serial("/dev/ttyS0", 38400, timeout = 10) # port may be ttyS0
        
        # Start threaded reading from Serial
        self.read_thread = threading.Thread(target=self.read_from_teensy, daemon=True)
        self.read_thread.start()

    def read_from_teensy(self):
        while 1:
            curr_line = self.serial_port.readline()
            try:    
                self.heading, self.left_encoder, self.right_encoder = self.parse_line(curr_line)
            except:
                continue
    def parse_line(self, line):
        """
            Current Line from the teensy (example):

            0 -69\t-0.03 -0.01 -0.01\t0.00 0.00 0.12\t186.69 -0.19 175.94\t0300\r\n
            
            Key:
            encoder left encoder right\tlinearaccel x y z\tgyroscope x y z\teuler x y \tcalibration\r\n
        """
        split_line = line.decode("utf-8").split('\t')

        # Get encoder values
        encoders = split_line[0].split(' ')
        left_encoder = int(encoders[0])
        right_encoder = int(encoders[1])

        # Get heading values
        euler = split_line[3].split(' ')
        heading = float(euler[0])

        return heading, left_encoder, right_encoder

    def get_heading(self):
        return self.heading
    
    def get_left_encoder_ticks(self):
        return self.left_encoder
    
    def get_right_encoder_ticks(self):
        return self.right_encoder

    def reset_encoders(self):
        self.serial_port.write(b'a') # writing anything will do

    def print_sensor_values(self):
        print("Heading: " + str(self.heading) + " Encoders: " + str(self.left_encoder) + " " + str(self.right_encoder))

def main():
    # Example usage of the class
    sensors = SensorsV2()
    i = 0
    while 1:
        sleep(0.1)
        sensors.print_sensor_values()
        i += 1

        if i % 100 == 0:
            sensors.reset_encoders()


if __name__ == "__main__":
    main()


