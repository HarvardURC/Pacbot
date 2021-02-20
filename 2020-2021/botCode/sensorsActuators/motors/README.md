These are classes for the motors on the raspberry pi. The motor pins (power and direction pins) are listed on pac_pins.cpp. 

To test the motors with motors_test.cpp, run in this directory:

gcc *.hpp *.cpp -o motors_test -lwiringPi -lstdc++ && ./motors_test
