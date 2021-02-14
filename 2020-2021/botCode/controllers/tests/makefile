# the compiler: gcc for C program, define as g++ for C++
CC = gcc 

# compiler flags:
#  -g    adds debugging information to the executable file
#  -Wall turns on most, but not all, compiler warnings
CFLAGS  = -lstdc++ -std=c++14 -o tests -Wall

TARGET = ./pid-test
MAIN = ../../
UTILS_C := $(wildcard $(MAIN)utils/*.cpp)
DATA_TYPES_C := $(wildcard $(MAIN)dataTypes/*.cpp)
ROBOT_STATE_C := $(wildcard $(MAIN)robotState/*.cpp)
SENSORS_ACTUATORS_C := $(wildcard $(MAIN)sensorsActuators/*.cpp)
CONTROLLERS_C := $(wildcard $(MAIN)controllers/*.cpp)
STATE_ESTIMATORS_C := $(wildcard $(MAIN)state_estimators/*.cpp)
STATE_UPDATERS_C := $(wildcard $(MAIN)state_updaters/*.cpp)

ORDERED := $(UTILS_C) $(DATA_TYPES_C) $(ROBOT_STATE_C)  $(SENSORS_ACTUATORS_C) $(CONTROLLERS_C) $(STATE_ESTIMATORS_C) $(STATE_UPDATERS_C) $(TARGET).cpp

all: $(TARGET)

$(TARGET):$(TARGET).cpp
	$(CC) $(CFLAGS) $(ORDERED)
clean:
	$(RM) $(TARGET)