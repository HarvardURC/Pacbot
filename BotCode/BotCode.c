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
#include <math.h>
//#include <wiringPi.h>
//#include <Direction.c> 
// Initialize connection with camera
//Must have two modes 

// Ineitialize Variables
	// need a variable to keep track of cardinal direction state
		// card_state = 1, 2, 3, 4. 1 being north, 2 being east, 3 being south, 4 being west
#define NORTH 	= 1;
#define EAST 	= 2;
#define SOUTH 	= 3;
#define WEST 	= 4;
//Pacman initial Position
#define ROW = 22;
#define COL = 13; 

//food opt = pellet =1, big pellet =  2 ; empty= 3; fruit = 4
typedef struct game_state
{
	cell_pos cur_pos; 
	int dir; 
}game_state;

//return type of getSuccessors
typedef struct sca{
	game_state state; 
	int cost;  
	int action; 

}status; 
typedef struct free_cell {
    cell_pos coordinates; 
    int pacman_pos;
    int ghost_pos;
    char food_opt; 
 	cell_pos adj_cell[4]; 
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
    while(fscanf (fp, "%d,%d,%c", &a, &b, &c)==3) {  
    	free_cell new_cell; 
    	new_cell.coordinates.cp_x = a; 
    	new_cell.coordinates.cp_y = b;
    	new_cell.pacman_pos = 0; 
    	new_cell.ghost_pos =0; 
    	new_cell.food_opt = c; 
    	new_cell.adj_cell[0].cp_x= 0; 
    	new_cell.adj_cell[1].cp_x = 0; 
    	new_cell.adj_cell[2].cp_x = 0; 
    	new_cell.adj_cell[3].cp_x= 0; 
    	new_cell.adj_cell[0].cp_y = 0; 
    	new_cell.adj_cell[1].cp_y = 0; 
    	new_cell.adj_cell[2].cp_y = 0; 
    	new_cell.adj_cell[3].cp_y = 0;   
    	new_cell.directions[0]= 0;
    	new_cell.directions[1]= 0; 
    	*(grid+b + 28*a) = new_cell;     
    }  

}
/*
````````````````````````````````````````````````````````````````````````````````
HEAP CODE
````````````````````````````````````````````````````````````````````````````````
*/
typedef struct node_t{
    int priority;
    sca * data;
} node_t;
 
typedef struct heap_t{
    node_t *nodes;
    int len;
    int size;
} heap_t;
 
void push (heap_t *h, int priority, game_state *data) {
    if (h->len + 1 >= h->size) {
        h->size = h->size ? h->size * 2 : 4;
        h->nodes = (node_t *)realloc(h->nodes, h->size * sizeof (node_t));
    }
    int i = h->len + 1;
    int j = i / 2;
    while (i > 1 && h->nodes[j].priority > priority) {
        h->nodes[i] = h->nodes[j];
        i = j;
        j = j / 2;
    }
    h->nodes[i].priority = priority;
    h->nodes[i].data = data;
    h->len++;
}
 
char *pop (heap_t *h) {
    int i, j, k;
    if (!h->len) {
        return NULL;
    }
    char *data = h->nodes[1].data;
    h->nodes[1] = h->nodes[h->len];
    h->len--;
    i = 1;
    while (1) {
        k = i;
        j = 2 * i;
        if (j <= h->len && h->nodes[j].priority < h->nodes[k].priority) {
            k = j;
        }
        if (j + 1 <= h->len && h->nodes[j + 1].priority < h->nodes[k].priority) {
            k = j + 1;
        }
        if (k == i) {
            break;
        }
        h->nodes[i] = h->nodes[k];
        i = k;
    }
    h->nodes[i] = h->nodes[h->len + 1];
    return data;
}
//N=1, E=2 S=3 W=4
sca * getSuccessors(game_state current_node){
	static sca successors[4];
	int x = current_node.cur_pos.cp_x; 
	int y = current_node.cur_pos.cp_y;
	int d = current_node.dir;
	for(int i = 0; i<4; i++){
		successors[i].state.cur_pos = grid[28*x + y].adj_cell[i];
		successors[i].action = i;
		if(d = i){
			successors[i].cost = 1;
		}
		else if((d-i)%2 == 0){
			successors[i].cost = 3;
		}
		else {
			successors[i].cost = 2;
		}
	}
	return successors; 
}

int manhattanDistance(cell_pos pos1, cell_pos pos2){
	int x1 = pos1.cp_x;
	int y1 = pos1.cp_y;
	int x2 = pos2.cp_x;
	int y2 = pos2.cp_y;
	return (abs(x1-x2) + abs(y1-y2));
}
/*
LINKED LIST CODE 
*/
typedef struct node {
    struct game_state* next;
    struct game_state* prev;
} node;

void insert_head(node* n) {
    n->next = head;
    n->prev = NULL;
    if (head)
        head->prev = n;
    head = n;
}

void remove(node* n) {
    if (n->next)
        n->next->prev = n->prev;
    if (n->prev)
        n->prev->next = n->next;
    else
        head = n->next;
}
//Use A* to get best next move in a sequence of moves
int getNextMove(game_state pac_pos, cell_pos target_pos){
	//Store all nodes on the tree fringe as a priority queue
	
	heap_t *fringe = (heap_t *)calloc(1, sizeof (heap_t));
	node_t cur_node; 
	cur_node.priority = manhattanDistance(pac_pos.coordinates, target_pos); 
	cur_node.data = pacman_pos; 
	push(new_node); 
	node * closed;
	while(1){
		cur_node = pop(fringe)
		if(cur_node==NULL)
			break;
		if((cur_node.data.coordinates.cp_x == target_pos.cp_x )&&(cur_node.data.coordinates.cp_y == target_pos.cp_y )){
			return;
		} else {

		}
	}  
	
    int i;	
}

int main(int argc, char** argv) {
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
