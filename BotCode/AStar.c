#include "AStar.h"
#include "state.h"
#include <math.h>
#include <stdlib.h>

node *head;

void push (heap_t *h, int priority, game_state *state) {
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
    h->nodes[i].data->state = *state;
    h->len++;
}
 
sca *pop (heap_t *h) {
    int i, j, k;
    if (!h->len) {
        return NULL;
    }
    sca *data = h->nodes[1].data;
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

void insert_head(node* n) {
    n->next = head;
    n->prev = NULL;
    if (head)
        head->prev = n;
    head = n;
}

void remove_node(node* n) {
    if (n->next)
        n->next->prev = n->prev;
    if (n->prev)
        n->prev->next = n->next;
    else
        head = n->next;
}
int contains(node * head, sca tar_sca){
    node * cur_sca = head; 
    while(cur_sca !=NULL){
        if(cur_sca->state == tar_sca)
    }
}
//Use A* to get best next move in a sequence of moves
node * head_closed; 
int getNextMove(game_state pac_pos, cell_pos target_pos){
	//Store all nodes on the tree fringe as a priority queue
	
	heap_t *fringe = (heap_t *)calloc(1, sizeof (heap_t));
	int prio = manhattanDistance(pac_pos.cur_pos, target_pos); 
	push(fringe, prio, &pac_pour_sca;
    int successors [4]; 
    noder_sca;
    node * curr_closed; 
       while(1){
        cur_sca = pop(fringe);
        if(cur_sca==NULL)
            break;
        if((cur_sca->state.cur_pos.cp_x == target_pos.cp_x )&&(cur_sca->state.cur_pos.cp_y == target_pos.cp_y )){
            //If hit goal state, return the head of the action list to get there
    cur_sca->action_lr_sca

action  } else {

        successors = getSuccessors()

             nt i;  
}


	}  
	
    int i;	
}

