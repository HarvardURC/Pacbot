# the compiler: gcc
CC = gcc

# compiler flags
# -g adds debugging information to the executable file
#  -Wall turns on most, but not all, compiler warnings
CFLAGS = -lstdc++ -std=c++14 -Wall -g -lwiringPi -lvl6180_pi

SENSORS_ACTUATORS_C := $(wildcard ../*.cpp)
SA_INTERFACE_C := $(wildcard ../sa_interface/*cpp)

TEST_SENSORS = sensors_test
TEST_MOTORS = motors_test

$(TEST_SENSORS):$(TEST_SENSORS).cpp
	$(CC) $(CFLAGS) -o $(TEST_SENSORS) $(TEST_SENSORS).cpp $(SENSORS_ACTUATORS_C) $(SA_INTERFACE_C)
$(TEST_MOTORS):$(TEST_MOTORS).cpp
	$(CC) $(CFLAGS) -o $(TEST_MOTORS) $(TEST_MOTORS).cpp $(SENSORS_ACTUATORS_C) $(SA_INTERFACE_C)

clean:
	$(RM) $(TEST_SENSORS) $(TEST_MOTORS)
