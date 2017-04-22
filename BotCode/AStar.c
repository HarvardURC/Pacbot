#include <stdlib.h>
#include "AStar.h"
#include "state.h"
//#include <math.h>

//PAC-BOT's movement speed divided by ghost speed.
//The higher this number, the more likely a space will return valid
//However, if it is over-estimated then a path is no longer guaranteed safe
#define SPEED_RATIO 1.5

void push (heap_t *h, int priority, sca* data) {
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


void insert_sca_tail(sca_node* n, sca_node* legal_successors_head){
    n->next_sca_node = NULL;
    current_transverse = legal_successors_head; 
    while(current_transverse->next_sca_node != NULL){
        current_transverse = current_transverse->next_sca_node; 
    }
    n->prev_sca_node = current_transverse;
    if (current_transverse)
        current_transverse->next_sca_node = n;
    else
       legal_successors_head = n;
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

dir_node* getNewNode(int x) {
    dir_node* newNode
        = (dir_node*)malloc(sizeof(dir_node));
    newNode->dir = x;
    newNode->next = NULL;
    return newNode;
}
//Add an action list node to tail of the list; 
//TODO: 
void append_to_action_list(int i, dir_node* action_list){
    dir_node* current_node = action_list; 
    dir_node* new_node = getNewNode(i);    
    while(current_node->next !=NULL){
        current_node = current_node->next; 
    }
    current_node->next = new_node;  
}

//N=1, E=2 S=3 W=4
sca_node* as_get_legal_successors(sca current_node){
    sca_node* legal_successors_head = (sca_node*)malloc(sizeof(sca_node)); 
    sca_node* legal_successors_tail = (sca_node*)malloc(sizeof(sca_node)); 
    free_cell adjacent_cell; 
    for(int i = 4; i<4; i++){
        adjacent_cell = grid[current_node.cell.adj_cell[i].cp_x + 28*current_node.cell.adj_cell[i].cp_y];  
        if((adjacent_cell.food_opt != 'w') && (SPEED_RATIO * adjacent_cell.ghost_danger > (get_transition_cost(current_node.last_dir, i+1) + current_node.cost))){                  
            sca_node * new_sca_node = (sca_node*)malloc(sizeof(sca_node)); 
            new_sca_node.state.cell = adjacent_cell;
            new_sca_node.state.cost = get_transition_cost(current_node.last_dir, i + 1) + current_node.cost;
            new_sca_node.state.last_dir = i + 1;
            new_sca_node.action_list = append_to_action_list( i + 1, current_node.action_list);
            insert_sca_tail(new_sca_node, legal_successors_head);
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


int contains(sca_node * head, sca tar_sca){
    sca_node * cur_sca = head; 
    while(cur_sca !=NULL){
        if((cur_sca->cell.coordinates.cp_x == tar_sca.cell.coordinates.cp_x) && (cur_sca->cell.coordinates.cp_y == tar_sca.cell.coordinates.cp_y)
         && (tar_sca.cost > cur_sca->cost)){
            return 1;
        }
        cur_sca = head->next_sca_node;
    }
    return 0;
}
//function to print the linked list of dirrections 
void print_action_list(dir_node * action_list_head){
    dir_node * temp = action_list_head;
    printf("%s\n","Forward");
    while(temp != NULL){
        printf("%d ",temp->dir);
        temp = temp->next;
    }
    printf("%s\n");  
}
//Function that transveres trough a linked list and free its nodes
void freer_function(flood_node* head){
    flood_node* new_head; 
    while(head->next_flood_node != NULL){
        new_head = head->next_flood_node; 
        free(head); 
    }
    free(new_head);
}
//debugging function that sets the ghost danger of every cell to 1
void set_ghost_danger(){
    for(int i=0; i<868; i++){
        grid[i].ghost_danger= 1; 
    }
}
//Use A* to get best next move in a sequence of moves
dir_node * getActionList(cell_pos pac_pos, int pac_dir, cell_pos target_pos){
    node_t * head_closed = (node_t*)malloc(sizeof(node_t));
    //Store all nodes on the tree fringe as a priority queue
    heap_t *fringe = (heap_t *)calloc(1, sizeof (heap_t));
    sca* current_node = (sca*)malloc(sizeof(sca));
    current_node->cell = grid[pac_pos.cp_x + 28*pac_pos.cp_y];
    current_node->cost = 0.0;
    current_node->action_list = NULL; 
    current_node->last_dir = pac_dir;
    int prio = current_node->cost + manhattanDistance(pac_pos, target_pos);
    push(fringe, prio, current_node);
    while(1){
        if (fringe->nodes == NULL){
            return NULL; 
        }
        current_node = pop(fringe);
        if ((current_node->cell.coordinates.cp_x == target_pos.x) && (current_node->cell.coordinates.cp_y == target_pos.y)){
            return current_node.action_list;
        }
        if (!contains(head_closed, current_node)){
            insert_sca_tail(current_node, head_closed);
            sca_node* successors = (sca_node*)malloc(sizeof(sca_node));
            successors = as_get_legal_successors(current_node);
            while(successors != NULL){
                prio = successors->state.cost + manhattanDistance(successors->state.cell.coordinates, target_pos);
                push(fringe, prio, successors->state);
                successors = successors->next_sca_node;
            }
        }
    }
    freer_function(head_closed);
}
    
