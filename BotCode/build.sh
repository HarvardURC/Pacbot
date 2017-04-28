gcc -std=gnu11 -c -o vl6180_pi.o vl6180_pi.c -I.;
gcc -std=gnu11 -c -o state.o state.c -I.;
gcc -std=gnu11 -c -o network.o network.c -I.;
gcc movement.c -o movement.o vl6180_pi.o -l wiringPi;
make;
