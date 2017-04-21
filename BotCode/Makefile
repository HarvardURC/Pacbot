CC=gcc
CFLAGS=-I.
DEPS = network.h
OBJ = BotCode.c network.o 

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

BotCode: $(OBJ)
	gcc -o $@ $^ $(CFLAGS)
