// Initialize libraries
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include <math.h>
#include <getopt.h>
#include <assert.h>
#include <time.h>
#include <sys/time.h>
#include "network.h"
#include "AStar.h"
#include "state.h"
#include "grid.h"
//#include <wiringPi.h>
//#include <Direction.c> 
// Initialize connection with camera
//Must have two modes 

// GLOBALS 
free_cell* grid; 
state_response* latest_state;

int main(int argc, char **arg) {

    latest_state = malloc(sizeof(state_response));
    if(latest_state == NULL) {
        return -1;
    }
    createGrid();

    struct state_response state;
    while(1) {
        //getState(&state);
        //printState(&state);
    }
        
    free(grid);
    return 0; 
}
 
