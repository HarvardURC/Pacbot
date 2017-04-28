CC=gcc -std=gnu11
CFLAGS=-I. 
DEPS = network.h state.h grid.h FloodFill.h desired_coordinates.h AStar.h pacbot_direction.h vl6180_pi.h wiringPiI2C.h
OBJ = BotCode.c network.o grid.o FloodFill.o state.o desired_coordinates.o AStar.o pacbot_direction.o  vl6180_pi.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS) -l wiringPi


BotCode: $(OBJ)
	gcc -o $@ $^ movement.o $(CFLAGS) -l wiringPi
	
