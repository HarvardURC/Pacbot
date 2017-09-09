#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "AStar.h"
#include "state.h"
//#include <math.h>

//PAC-BOT's movement speed divided by ghost speed.
//The higher this number, the more likely a space will return valid
//However, if it is over-estimated then a path is no longer guaranteed safe
#define SPEED_RATIO 1.5

static void push (heap_t *h, int priority, sca* data) {
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
 
static sca *pop (heap_t *h) {
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

static double get_transition_cost(int pac_dir, int intended_dir){
    if (pac_dir == intended_dir){
        return 1.0;
    }
    else if ((pac_dir - intended_dir)%4 == 2) {
        return 3.0;
    }
    else {
        return 2.0; 
    }
}

int manhattanDistance(cell_pos pos1, cell_pos pos2) {
    int x1 = pos1.cp_x;
    int y1 = pos1.cp_y;
    int x2 = pos2.cp_x;
    int y2 = pos2.cp_y;
    return (abs(x1-x2) + abs(y1-y2));
}

//N=1, E=2, S=3, W=4, STOP = 5
static void as_add_legal_successors(sca* current_node, heap_t *fringe,
        uint16_t *costs, int ignore_ghosts, cell_pos target_pos) {
    free_cell adjacent_cell; 
    double action_cost;
    int i;
    for(i = 0; i<4; i++){
        adjacent_cell = grid[current_node->cell.adj_cell[i].cp_y + 28 * current_node->cell.adj_cell[i].cp_x];  
        action_cost = get_transition_cost(current_node->actions[current_node->next_action-1], i+1) + current_node->cost;
        if((adjacent_cell.food_opt != 'w') && (ignore_ghosts || 
                (SPEED_RATIO * adjacent_cell.ghost_danger > action_cost)) &&
                action_cost < *(costs+current_node->cell.adj_cell[i].cp_y + 28 * current_node->cell.adj_cell[i].cp_x)) {                  
            *(costs+current_node->cell.adj_cell[i].cp_y + 28 * current_node->cell.adj_cell[i].cp_x) = action_cost;
            sca *new_sca = malloc(sizeof(sca)); 
            new_sca->cell = adjacent_cell;
            new_sca->cost = action_cost;
            memcpy(&new_sca->actions[0], &current_node->actions[0], sizeof(uint8_t) * 200);
            new_sca->actions[current_node->next_action] = i + 1 ;
            new_sca->next_action = current_node->next_action+1;
            if (new_sca->next_action == 200) {
                // too many actions. We can't handle this path.
                free(new_sca);
            } else {
                int prio = manhattanDistance(adjacent_cell.coordinates, target_pos) + action_cost;
                push(fringe, prio, new_sca);
            }
            
        }
    }
}

// Use A* to get best next move in a sequence of moves
int getActionList(cell_pos pac_pos, int pac_dir, cell_pos target_pos,
        int ignore_ghosts, uint8_t *res) {
    //Store all nodes on the tree fringe as a priority queue
    heap_t *fringe = (heap_t *)calloc(1, sizeof (heap_t));
    sca* cur_dat = malloc(sizeof(sca));
    cur_dat->cell = grid[pac_pos.cp_y + 28*pac_pos.cp_x];
    cur_dat->cost = 0.0;
    cur_dat->actions[0] = pac_dir;
    cur_dat->next_action = 1;
    int prio = manhattanDistance(pac_pos, target_pos);
    push(fringe, prio, cur_dat);
    uint16_t costs[868];
    int i;
    for (i = 0; i <868; i++) {
        costs[i] = 4096;
    }
    *(costs+28*pac_pos.cp_x + pac_pos.cp_y) = 0;
    while(1){
        if (fringe->nodes == NULL){
            return 1; 
        }
        cur_dat = pop(fringe);
        if (cur_dat == NULL) {
            break;
        }
        if ((cur_dat->cell.coordinates.cp_x == target_pos.cp_x) &&
                (cur_dat->cell.coordinates.cp_y == target_pos.cp_y)){
            memcpy(res, &cur_dat->actions[0], sizeof(uint8_t) * 200);
            *(res + cur_dat->next_action) = 5;
            while (fringe->len != 0){
                cur_dat = pop(fringe);
                free(cur_dat);
            }
            free(fringe->nodes);
            free(fringe);
            return 0;

        }
        as_add_legal_successors(cur_dat, fringe, &costs[0], ignore_ghosts, target_pos);
        free(cur_dat);
    }
    free(fringe->nodes);
    free(fringe);
    return 1;
}
