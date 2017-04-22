CC=gcc -std=gnu11
CFLAGS=-I. 
DEPS = network.h state.h AStar.h grid.h FloodFill.h
OBJ = BotCode.c network.o AStar.o grid.o  FloodFill.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

BotCode: $(OBJ)
	gcc -o $@ $^ $(CFLAGS)
