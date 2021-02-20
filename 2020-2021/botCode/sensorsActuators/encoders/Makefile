
CC = g++
CFLAGS = -O2

objects = rs232.o

encoder: $(objects) encoder.o
	$(CC) $(objects) encoder.o -o encoder

encoder.o: encoder.cpp rs232.h
	$(CC) $(CFLAGS) -c encoder.cpp -o encoder.o

rs232.o : rs232.h rs232.c
	$(CC) $(CFLAGS) -c rs232.c -o rs232.o

clean :
	$(RM) test_rx test_tx $(objects) demo_rx.o demo_tx.o rs232.o

