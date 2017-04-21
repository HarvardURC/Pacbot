CC=gcc
CFLAGS=-I.
DEPS = network.h state.h AStar.h grid.h
OBJ = BotCode.c network.o AStar.o grid.o state.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

BotCode: $(OBJ)
	gcc -o $@ $^ $(CFLAGS)
