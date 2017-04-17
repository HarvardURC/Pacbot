// Initialize libraries
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


// Initialize connection with camera


// Initialize Variables

	// need a variable to keep track of cardinal direction state
		// card_state = 1, 2, 3, 4. 1 being north, 2 being east, 3 being south, 4 being west

// Initialize Grid

typedef struct cell_status {
    int pacman_pos;
    int ghost_pos;
    char food_opt;  
} cell_status;

int main(int argc, char* argv[]) {
	char* grid =  malloc(sizeof(cell_status)*31*28);


	return 0; 
}

// Update Grid

	// starting grid

/*

walls

(0,0) (1,0) (2,0) (3,0) (4,0) (5,0) (6,0) (7,0) (8,0) (9,0) 
(10,0) (11,0) (12,0) (13,0) (14,0) (15,0) (16,0) (17,0) (18,0) (19,0) 
(20,0) (21,0) (22,0) (23,0) (24,0) (25,0) (26,0) (27,0) 

(0,1) (27,1)

(0,2) (2,2) (3,2) (4,2) (5,2) (6,2) (7,2) (8,2) (9,2) (10,2) (11,2) (13,2) 
(14,2) (16,2) (17,2) (18,2) (19,2) (20,2) (21,2) (22,2) (23,2) (24,2) (25,2) (27,2) 

(0,3) (2,3) (3,3) (4,3) (5,3) (6,3) (7,3) (8,3) (9,3) (10,3) (11,3) (13,3) 
(14,3) (16,3) (17,3) (18,3) (19,3) (20,3) (21,3) (22,3) (23,3) (24,3) (25,3) (27,3)

(0,4) (7,4) (8,4) (13,4) (14,4) (19,4) (20,4) (27,4)

(0,5) (1,5) (2,5) (4,5) (5,5) (7,5) (8,5) (10,5) (11,5) (12,5) (13,5) (14,5) (15,5)
(16,5) (17,5) (19,5) (20,5) (22,5) (23,5) (25,5) (26,5) (27,5) 

(0,6) (1,6) (2,6) (4,6) (5,6) (7,6) (8,6) (10,6) (11,6) (12,6) (13,6) (14,6) (15,6)
(16,6) (17,6) (19,6) (20,6) (22,6) (23,6) (25,6) (26,6) (27,6) 



(0,30) (1,30) (2,30) (3,30) (4,30) (5,30) (6,30) (7,30) (8,30) (9,30) 
(10,30) (11,30) (12,30) (13,30) (14,30) (15,30) (16,30) (17,30) (18,30) (19,30) 
(20,30) (21,30) (22,30) (23,30) (24,30) (25,30) (26,30) (27,30) 

*/ 

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
