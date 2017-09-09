#ifndef _FLOOD_FILL_H_
#define _FLOOD_FILL_H_

#include <math.h>
#include <stdlib.h>
#include <limits.h>
#include <stdio.h>
#include "state.h"
#include "grid.h"
#include "AStar.h"


//Queue for fringe, also used for the closed list and successor list
typedef struct flood_node{
	struct flood_node *next_flood_node;
	free_cell current_cell;  
    int depth;
} flood_node; 


//Returns the head node and moves head pointer to next node
int pop_flood_node(flood_node **head, flood_node **tail, flood_node **ret);

void add_legal_successors(int new_depth, free_cell pos, uint8_t *visited,
        flood_node **head, flood_node **tail, int g_dir);

void clear_ghost_danger();
//on new ghost position update, change the main grid danger variable to match distance from ghosts
void ghost_flood(ghost_dir *direcs);

#endif /* _FLOOD_FILL_H_ */
