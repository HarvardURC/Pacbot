# the compiler: gcc for C program, define as g++ for C++
CC = gcc 

# compiler flags:
#  -g    adds debugging information to the executable file
#  -Wall turns on most, but not all, compiler warnings
CFLAGS  = -lstdc++ -lpthread -std=c++17 -o tests -Wall

TARGET = ./test-master

MAIN = ../
UTILS_C := $(wildcard $(MAIN)utils/*.cpp)
DATA_TYPES_C := $(wildcard $(MAIN)dataTypes/*.cpp)
ROBOT_STATE_C := $(wildcard $(MAIN)robotState/*.cpp)
SA_INTERFACE_C := $(wildcard $(MAIN)sensorsActuators/sa_interface/*.cpp)
SENSORS_ACTUATORS_C := $(wildcard $(MAIN)sensorsActuators/*.cpp)
CONTROLLERS_C := $(wildcard $(MAIN)controllers/*.cpp)
STATE_JUDGES_C := $(wildcard $(MAIN)stateJudges/*.cpp)
STATE_ESTIMATORS_C := $(wildcard $(MAIN)stateEstimators/*.cpp)

CONTROLLERS_TESTS := $(wildcard controllers/*.cpp)
DATATYPES_TESTS := $(wildcard dataTypes/*.cpp)

ORDERED := $(UTILS_C) $(DATA_TYPES_C) $(SA_INTERFACE_C) $(ROBOT_STATE_C) $(CONTROLLERS_C) $(STATE_JUDGES_C) $(STATE_ESTIMATORS_C) $(SENSORS_ACTUATORS_C) $(DATATYPES_TESTS) $(CONTROLLERS_TESTS) $(TARGET).cpp

all: $(TARGET)

$(TARGET):$(TARGET).cpp
	$(CC) $(CFLAGS) $(ORDERED)
clean:
	$(RM) $(TARGET)