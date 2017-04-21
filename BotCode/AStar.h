#ifndef _ASTAR_H_
#define _ASTAR_H_

#include "state.h"

//return type of getSuccessors
typedef struct sca{
	game_state state; 
	int cost;  
	int action; 

} sca; 

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
 
void push (heap_t *h, int priority, game_state *state);

sca *pop (heap_t *h);

sca * getSuccessors(game_state current_node);

int manhattanDistance(cell_pos pos1, cell_pos pos2);

/*
LINKED LIST CODE 
*/
typedef struct node {
    struct node* prev;
    struct node* next;
    struct game_state* state;
} node;

void insert_head(node* n);

void remove_node(node* n);

int getNextMove(game_state pac_pos, cell_pos target_pos);

#endif /* _ASTAR_H_*/
