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
#include <stdio.h>
#include "network.h"
#include "AStar.h"
#include "state.h"
#include "grid.h"
#include <math.h>
//#include <wiringPi.h>
//#include <Direction.c> 
// Initialize connection with camera
//Must have two modes 

// GLOBALS 
free_cell *grid; 
state_response *latest_state;

int main(int argc, char** argv) {
    latest_state = malloc(sizeof(state_response));
    if(latest_stae == NULL) {
        return 1;
    }
	createGrid();

	int i = manhattanDistance(grid[30].coordinates, grid[45].coordinates);
	printf("%d\n", i);

	for(int i=0; i<868; i++){
		printf("(%d,%d)",grid[i].coordinates.cp_x, grid[i].coordinates.cp_y);
		if(i%28==0)
		printf("\n");
	}
   
    // struct state_response state;
    // while(1) {
    //    getState(&state);
    //    printState(&state);
    // }
    
    free(grid);

	return 0; 
}
 // incoming camera updates

// Output Grid as variables (a tuple maybe?) for determining strategies


// Module for determining behaviors, used in "Early Game" and "Late Game"

	// Avoid
		// 

	// Lure
		// Should include implementation on when to eat power pellet

	// Engage
		// Should just focus on chasing. Power pellet is already eaten in this state

	// Suicide 
		// memes

// Early game (# of pellets on board > N) 

	// Focus on Bottom Left Corner

		// if in danger, avoid. But don't avoid otherwise
		// if # of pellets < N, start luring
		// 

// Late game (not late game) 
	
	// No specific focus, so don't override avoid
		// 


// Feed move module with strategy

	// If suicide = true, override following and find danger!
		// If danger = 1, override everything with avoid
		// 

// Move module
	// if move_north == true

		// if card_state == 1
			// move forward
		// if card_state == 2
			// angle -90
			// move forward
		// if card_state == 3
			// angle 180
			// move forward
		// if card_state = 4
			// angle 90	
			// move forward

	// else if move_east == true

		// if card_state == 1
			// angle 90
			// move forward
		// if card_state == 2
			// move forward
		// if card_state == 3
			// angle -90
			// move forward
		// if card_state = 4
			// angle 180
			// move forward

	// else if move_south = true

		// if card_state == 1
			// angle 180
			// move forward
		// if card_state == 2
			// angle 90
			// move forward
		// if card_state == 3
			// angle 0
			// move forward
		// if card_state = 4
			// angle -90
			// move forward

	// else if move_west = true

		// if card_state == 1
			// angle -90 
			// move forward
		// if card_state == 2
			// angle 180
			// move forward
		// if card_state == 3
			// angle 90
			// move forward
		// if card_state = 4
			// move forward
