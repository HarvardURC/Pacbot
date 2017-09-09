#ifndef _ASTAR_H_
#define _ASTAR_H_

#include <inttypes.h>
#include "state.h"

//N=1, E=2, S=3, W=4, STOP = 5
typedef struct sca{
    free_cell cell; 
    double cost; 
    uint8_t actions[200]; 
    uint8_t next_action;
} sca; 

/*
`````````````````````````````````````
HEAP CODE (Priority Queue)
`````````````````````````````````````
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

int manhattanDistance(cell_pos pos1, cell_pos pos2);

/*
 *  Use A* to get best next move in a sequence of moves
 *
 *  Params:
 *  - ignore_ghosts: If 0 - will not ignore ghosts. if 1, will ignore.
 *  - res: a pointer to an array of 200 uint8_t's.
 */
int getActionList(cell_pos pac_pos, int pac_dir, cell_pos target_pos,
        int ignore_ghosts, uint8_t *res);

#endif /* _ASTAR_H_*/
