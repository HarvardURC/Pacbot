# the compiler: gcc for C program, define as g++ for C++
CC = gcc 

# compiler flags:
#  -g    adds debugging information to the executable file
#  -Wall turns on most, but not all, compiler warnings
CFLAGS  = -lstdc++ -std=c++14 -o executable -Wall

MAIN := .
UTILS_C := $(wildcard utils/*.cpp)
DATA_TYPES_C := $(wildcard dataTypes/*.cpp)
ROBOT_STATE_C := $(wildcard robotState/*.cpp)
SENSORS_ACTUATORS_C := $(wildcard sensorsActuators/*.cpp)
CONTROLLERS_C := $(wildcard controllers/*.cpp)
STATE_ESTIMATORS_C := $(wildcard state_estimators/*.cpp)
STATE_UPDATERS_C := $(wildcard state_updaters/*.cpp)
MAIN_FILES_C := $(wildcard $(MAIN)/*.cpp)

DEPENDENCIES := wiringPi.c
ORDERED := $(UTILS_C) $(DATA_TYPES_C) $(ROBOT_STATE_C)  $(SENSORS_ACTUATORS_C) $(CONTROLLERS_C) $(STATE_ESTIMATORS_C) $(STATE_UPDATERS_C) $(MAIN_FILES_C)


# the build target executable:
TARGET = master

all: $(TARGET)

$(TARGET):$(TARGET).cpp
	$(CC) $(DEPENDENCIES) $(CFLAGS) $(ORDERED)
clean:
	$(RM) $(TARGET)