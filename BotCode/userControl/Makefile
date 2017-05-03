CC=gcc
CFLAGS= -g -I. 
DEPS = network.h movement.h vl6180_pi.h wiringPiI2C.h 
OBJ = user_control.o network.o movement.o vl6180_pi.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS) -l wiringPi


BotCode: $(OBJ)
	gcc -o $@ $^ $(CFLAGS) -l wiringPi
	
