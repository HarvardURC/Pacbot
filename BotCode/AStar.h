#ifndef _ASTAR_H_
#define _ASTAR_H_

#include "state.h"

//return type of getSuccessors
typedef struct dir_node
{
    int dir; 
    struct dir_node * next; 
} dir_node;

void append_to_action_list(int i, dir_node * action_list);

typedef struct sca{
    free_cell cell; 
    double cost; 
    dir_node * action_list; 
    int last_dir;
} sca; 

/*
````````````````````````````````````````````````````````````````````````````````
HEAP CODE (Priority Queue)
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
 
void push (heap_t *h, int priority, sca * data);

sca *pop (heap_t *h);

sca * as_get_legal_successors(sca current_node);

double get_transition_cost(int pac_dir, int intended_dir);

int manhattanDistance(cell_pos pos1, cell_pos pos2);

/*
CLosed Node LINKED LIST CODE 
*/
typedef struct sca_node {
    struct sca_node* prev_sca_node;
    struct sca_node* next_sca_node;
    struct sca state;
} sca_node;

void insert_head(sca_node* n);

void insert_sca_tail(sca_node* n, sca_node* legal_successors_tail, sca_node* legal_successors_head);

void remove_node(sca_node* n);

dir_node * getActionList(cell_pos pac_pos, int pac_dir, cell_pos target_pos);

#endif /* _ASTAR_H_*/
