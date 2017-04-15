#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <inttypes.h>
#include <math.h>
#include <getopt.h>
#include <assert.h>
#include <time.h>
#include <sys/time.h>
#include <Motors.h>


//Structure definition that will contain the three commands 
typedef struct cell_status {
    int pacman_pos;
    int ghost_pos;
    char food_opt;  
} cell_status;

int main(int argc, char* argv[]) {
	char* grid =  malloc(sizeof(cell_status)*31*27);


	return 0; 
}
