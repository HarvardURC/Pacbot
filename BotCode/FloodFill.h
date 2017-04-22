#include <math.h>
#include <stdlib.h>
#include <limits.h>
#include <stdio.h>
#include "state.h"
#include "grid.h"
#include "AStar.h"


//Queue for fringe, also used for the closed list and successor list
typedef struct flood_node{
	struct flood_node * next_flood_node;
	free_cell current_cell;  
}flood_node; 

//Add a node to the end of 
void push_flood_node(flood_node* n, flood_node * current_node); 
//Returns the head node and moves head pointer to next node
free_cell pop_flood_node(flood_node* head);
//returns 0 if our list does not contain pos 1 if it does 
int  closed_contains(free_cell cell, flood_node * n);
//returns up to four possible next moves
flood_node * get_legal_successors(free_cell cell, int depth); 
//set the ghost danger of every square to max_int
void clear_ghost_danger();
//on new ghost position update, change the main grid danger variable to match distance from ghosts
void ghost_flood(state_response state);  
