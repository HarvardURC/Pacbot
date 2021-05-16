# compiler: gcc for C program
CC = gcc

# compiler flags:
CFLAGS  = -std=c++14 -Wall
DEPENDENCIES = -lstdc++ -lpthread 

MAIN := .
UTILS_C := $(wildcard utils/*.cpp)
DATA_TYPES_C := $(wildcard dataTypes/*.cpp)
ROBOT_STATE_C := $(wildcard robotState/*.cpp)
SA_INTERFACE_C := $(wildcard sensorsActuators/sa_interface/*.cpp)
SENSORS_ACTUATORS_C := $(wildcard sensorsActuators/*.cpp)
CONTROLLERS_C := $(wildcard controllers/*.cpp)
STATE_JUDGES_C := $(wildcard stateJudges/*.cpp)
STATE_ESTIMATORS_C := $(wildcard stateEstimators/*.cpp)
MAIN_FILES_C := $(wildcard $(MAIN)/*.cpp)

TARGET = master

ORDERED := $(UTILS_C) $(DATA_TYPES_C) $(SA_INTERFACE_C) $(ROBOT_STATE_C) $(CONTROLLERS_C) $(STATE_JUDGES_C) $(STATE_ESTIMATORS_C) $(SENSORS_ACTUATORS_C) $(MAIN_FILES_C)

# this replaces .cpp with .o for object files
OBJS = $(ORDERED:.cpp=.o)

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(DEPENDENCIES) $(CFLAGS) $(ORDERED) -o executable

.cpp.o:
	$(CC) $(DEPENDENCIES) $(CFLAGS) -c $< -o $@

clean:
	$(RM) $(OBJS) 
