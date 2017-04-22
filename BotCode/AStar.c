#include "AStar.h"
#include "state.h"
//#include <math.h>
#include <stdlib.h>

void push (heap_t *h, int priority, sca*data) {
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
/*
LINKED LIST CODE 
*/

void insert_head(sca* n, sca * legal_successors_head) {
    n->next = legal_successors_head;
    n->prev = NULL;
    if (legal_successors_head)
        legal_successors_head->prev = n;
    legal_successors_head= n;
}
void insert_sca_tail(sca_node* n, sca_node* legal_successors_tail, sca_node* legal_successors_head){
    n->next_sca_node = NULL;
    n->prev_sca_node = legal_successors_tail;
    if (legal_successors_tail)
        legal_successors_tail->next_sca_node = n;
    else
       legal_successors_head = n;
    legal_successors_tail = n;
}
void remove_node(node* n) {
    if (n->next)
        n->next->prev = n->prev;
    if (n->prev)
        n->prev->next = n->next;
    else
        head = n->next;
}
double get_transition_cost(int pac_dir, int intended_dir){
    if (pac_dir == intended_dir){
        return 1.0
    }
    else if ((pac_dir - intended_dir)%4 == 2) {
        return 3.0
    }
    else {
        return 2.0
    }
}
//Check we are transversing the linked list correctly 
void append_to_action_list(int i, dir_node* action_list){
    dir_node* current_node = action_list; 
    dir_node new_node; 
    new_node->dir = i; 
    new_node->next =NULL; 
    while(current_node->next !=NULL){
        current_node = current_node->next; 
    }
    current_node->next = new_node;
    current_node = new_node;  
}
//N=1, E=2 S=3 W=4
sca_node* get_legal_successors(sca current_node){
    sca_node* legal_successors_head; 
    sca_node* legal_successors_tail; 
    free_cell adjacent_cell; 
    for(int i = 0; i<4; i++){
        adjacent_cell = grid[current_node.cell.adj_cell[i].cp_x + 28*current_node.cell.adj_cell[i].cp_y];  
        if((adjacent_cell.food_opt != 'w') && (adjacent_cell.ghost_danger > get_transition_cost(current_node.last_dir, i) + current_node.cost)){                  
            sca_node * new_sca_node; 
            new_sca_node.state.cell = adjacent_cell;
            new_sca_node.state.cost = get_transition_cost(current_node.last_dir, i) + current_node.cost;
            new_sca_node.state.last_dir = i;
            new_sca_node.action_list = append_to_action_list(i, current_node.action_list);
            insert_sca_tail(new_sca_node, legal_successors_tail, legal_successors_head);
        }

    }
    
    return legal_successors_head; 
}


int manhattanDistance(cell_pos pos1, cell_pos pos2){
    int x1 = pos1.cp_x;
    int y1 = pos1.cp_y;
    int x2 = pos2.cp_x;
    int y2 = pos2.cp_y;
    return (abs(x1-x2) + abs(y1-y2));
}


int contains(node * head, sca tar_sca){
    node * cur_sca = head; 
    while(cur_sca !=NULL){
        if(cur_sca->state == tar_sca)
    }
}
//Use A* to get best next move in a sequence of moves

dir_node * getActionList(cell_pos pac_pos, int pac_dir, cell_pos target_pos){
    node_t * head_closed;
	//Store all nodes on the tree fringe as a priority queue
	heap_t *fringe = (heap_t *)calloc(1, sizeof (heap_t));
    sca * current_node;
    *current_node.cell = grid[pac_pos.cp_x + 28*pac_pos.cp_y];
    *current_node.cost = 0.0;
    *current_node.action_list = NULL; //Ask Magaly if this is ok
    *current_node.last_dir = pac_dir;
    int prio = current_node.cost + manhattanDistance(pac_pos, target_pos);
    push(fringe, prio, current_node);
    while(1){
        if (fringe.nodes == NULL){
                break; 
        }
        *current_node = pop(fringe);

    }
}
    
