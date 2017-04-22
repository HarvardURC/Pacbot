CC=gcc -std=gnu11
CFLAGS=-I. 
DEPS = network.h state.h grid.h FloodFill.h desired_coordinates.h AStar.h
OBJ = BotCode.c network.o grid.o FloodFill.o state.o desired_coordinates.o AStar.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

BotCode: $(OBJ)
	gcc -o $@ $^ $(CFLAGS)
