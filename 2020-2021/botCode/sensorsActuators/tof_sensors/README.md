Container here are classes for the time of flights sensors on the PacBot. The library vl6180 should be cloned onto the PacBot at this directory; installing the vl6180 library is another option.

To run sensors_test.cpp, run:

gcc *.hpp *.cpp -lwiringPi -lvl6180_pi -lstdc++
