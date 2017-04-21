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
//#include <wiringPi.h>
//#include <Direction.c> 


// Initialize connection with camera
//Must have two modes 

// Initialize Variables

	// need a variable to keep track of cardinal direction state
		// card_state = 1, 2, 3, 4. 1 being north, 2 being east, 3 being south, 4 being west
#define NORTH 	= 1;
#define EAST 	= 2;
#define SOUTH 	= 3;
#define WEST 	= 4;
//Pacman initial Position
#define ROW = 22;
#define COL = 13; 
typedef struct cell_cordinates{
	int y; 
	int x;
}cell_cordinates;
//food opt = pellet =1, big pellet =  2 ; empty= 3; fruit = 4  
typedef struct game_state
{
	cell_cordinates cur_pos; 
	int dir; 
}game_state;

typedef struct free_cell {
    cell_cordinates cordinates; 
    int pacman_pos;
    int ghost_pos;
    char food_opt; 
 	cell_cordinates adj_cell[4]; 
    int directions[4]; 
}free_cell;

// Declare Grid as global 
free_cell *grid; 
void createGrid(){
	grid = (free_cell*) malloc(868*sizeof(free_cell)); 
    FILE *fp;
    int a; 
    int b; 
    char c;  
    fp = fopen("freespaces.txt", "r"); // I open the file to read it("r")
    while(fscanf (fp, "%d,%d,%s", &a, &b, &c)==3) {  
    	free_cell new_cell; 
    	new_cell.cordinates.x = a; 
    	new_cell.cordinates.y = b;
    	new_cell.pacman_pos = 0; 
    	new_cell.ghost_pos =0; 
    	new_cell.food_opt = c; 
    	new_cell.adj_cell[0].x = 0; 
    	new_cell.adj_cell[1].x = 0; 
    	new_cell.adj_cell[2].x = 0; 
    	new_cell.adj_cell[3].x = 0; 
    	new_cell.adj_cell[0].y = 0; 
    	new_cell.adj_cell[1].y = 0; 
    	new_cell.adj_cell[2].y = 0; 
    	new_cell.adj_cell[3].y = 0;   
    	new_cell.directions[0]= 0;
    	new_cell.directions[1]= 0; 
    	grid[b + 28*a] = new_cell;     
    }
   

}
//N=1, E=2 S=3 W=4
game_state * get_successor(game_state current_node){
	static game_state successors[4];
	int x = current_node.cur_pos.x; 
	int y = current_node.cur_pos.y;
	int d = current_node.dir; 
	for(int i = 0; i<4; i++)
		successors[i].cur_pos = grid[28*x + y].adj_cell[i]; 
	return successors; 
}

int main(int argc, char** argv) {
	createGrid();
	for(int i=0; i<=31; i++){
		for(int j=0; j<28; j++){
				printf("(%d,%d)",grid[j*28 + i].cordinates.x, grid[j*28 + i].cordinates.y);
		}
		printf("\n");
	}

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
