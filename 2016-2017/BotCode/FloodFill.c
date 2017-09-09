#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>
#include <string.h>
#include "grid.h"
#include "state.h"
#include "AStar.h"
#include "FloodFill.h"

//Returns the head node and moves head pointer to next node
int pop_flood_node(flood_node **head, flood_node **tail, flood_node **ret){
	if(*head == NULL) {
        return 1; 
    }
	*ret = *head;
    *head = (*head)->next_flood_node;
    if (*head == NULL) {
        *tail = NULL;
    }
	return 0;
}

static int opposite(int a_dir, int b_dir) {
    if ((a_dir == 1 && b_dir == 3) ||
        (a_dir == 2 && b_dir == 4) ||
        (a_dir == 3 && b_dir == 1) ||
        (a_dir == 4 && b_dir == 2)) {
        return 1;
    }
    return 0;
}

//returns up to four possible next moves
void add_legal_successors(int new_depth, free_cell pos, uint8_t *visited,
        flood_node **head, flood_node **tail, int g_dir) {
    //printf("Entered add_legal_successors\n");
	free_cell adjacent_cell;
    //printf("Declared adjacent_cell\n");
    int i;
    //printf("Declared int i\n");
	for(i=0; i<4; i++){
        //printf("Entered for loop\n");
        //int x_coord = pos.adj_cell[i].cp_x;
        //int y_coord = pos.adj_cell[i].cp_y;
        //printf("X Coordinate to access: %d \n", x_coord);
        //printf("Y Coordinate to access: %d \n", y_coord);
		adjacent_cell = grid[28*pos.adj_cell[i].cp_x +pos.adj_cell[i].cp_y];  
        //printf("Initialized adjacent_cell\n");
		if( (adjacent_cell.food_opt != 'w') && 
                !(new_depth == 1 && opposite(g_dir, i+1)) &&
                (*(visited+28*pos.adj_cell[i].cp_x + pos.adj_cell[i].cp_y) != 1)) {
            *(visited+28*pos.adj_cell[i].cp_x + pos.adj_cell[i].cp_y) = 1;
			flood_node *new_flood_node = malloc(sizeof(flood_node));
            if (new_flood_node == NULL) {
                printf("EOM. can't handle\n");
                exit(1);
            }
			new_flood_node->current_cell = adjacent_cell; 
			new_flood_node->next_flood_node = NULL; 
            new_flood_node->depth = new_depth;
            if (*head == NULL) {
                *head = new_flood_node;
                *tail = *head;
            } else if (*head == *tail) {
                (*head)->next_flood_node = new_flood_node;
                *tail = new_flood_node;
            } else {
                (*tail)->next_flood_node = new_flood_node;
                *tail = new_flood_node;
            }
		}
	}
}

void clear_ghost_danger(){
    int i;
	for(i=0; i<868; i++){
		grid[i].ghost_danger = 255; 
	}
}

//on new ghost position update, change the main grid danger variable to match distance from ghosts
void ghost_flood(ghost_dir *direcs) {
	cell_pos ghosts [4]; 
    
	ghosts[0] = getInky();
	ghosts[1] = getBlinky();
	ghosts[2] = getPinky();
	ghosts[3] = getClyde();
    /* 
    ghosts[0].cp_x = 1;//getInky();
	ghosts[0].cp_y = 1; 
	ghosts[1].cp_x = 1;//getBlinky();
	ghosts[1].cp_y = 1;
	ghosts[2].cp_x = 1; 
	ghosts[2].cp_y = 1;  //getPinky();
	ghosts[3].cp_x = 1;
	ghosts[3].cp_y = 1; //getClyde();
    */
    int directions[4];
    directions[0] = direcs->ink_dir;
    directions[1] = direcs->blink_dir;
    directions[2] = direcs->pink_dir;
    directions[3] = direcs->clyde_dir;
    uint8_t visited[868];
	clear_ghost_danger();
    int i;
	for(i=0; i<4; i++) {
        memset(&visited[0], 0, sizeof(uint8_t) * 868); 
		flood_node *head_fringe = (flood_node*) malloc(sizeof(flood_node));
        if (head_fringe == NULL) {
            printf("EOM. can't handle\n");
            exit(1);
        }
		flood_node *tail = head_fringe;
        free_cell temp = grid[28*ghosts[i].cp_x + ghosts[i].cp_y];
		head_fringe->current_cell =  temp;
        *(visited+28*ghosts[i].cp_x + ghosts[i].cp_y) = 1;
		head_fringe->depth = 0;
        head_fringe->next_flood_node = NULL;
		while (1) {
            flood_node *cur_node;
			if(head_fringe == NULL) {
				break; 
			}

            int empty = pop_flood_node(&head_fringe, &tail, &cur_node);
            if (empty) {
                printf("should not reach here!\n");
            }
			add_legal_successors(cur_node->depth+1, cur_node->current_cell,
                    &visited[0], &head_fringe, &tail, directions[i]);
            if (grid[28*cur_node->current_cell.coordinates.cp_x +
                    cur_node->current_cell.coordinates.cp_y].ghost_danger > cur_node->depth) {
			    grid[28*cur_node->current_cell.coordinates.cp_x +
                    cur_node->current_cell.coordinates.cp_y].ghost_danger = cur_node->depth; 
            }
            free(cur_node);
		}
	}
}

