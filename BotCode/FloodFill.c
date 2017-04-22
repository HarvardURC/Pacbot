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

//returns up to four possible next moves
void add_legal_successors(int new_depth, free_cell pos, uint8_t *visited, flood_node **head, flood_node **tail, int direc){
	free_cell adjacent_cell;
	for(int i=0; i<4; i++){
		adjacent_cell = grid[28*pos.adj_cell[i].cp_x +pos.adj_cell[i].cp_y];  
		if( (adjacent_cell.food_opt != 'w') &&
                (*(visited+28*pos.adj_cell[i].cp_x + pos.adj_cell[i].cp_y) != 1) && direc != (i + 2) % 4) {
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
	for(int i=0; i<868; i++){
		grid[i].ghost_danger = 255; 
	}
}

//on new ghost position update, change the main grid danger variable to match distance from ghosts
void ghost_flood(/*ghost_dir* direcs*/){
	cell_pos ghosts [4]; 
    /*
	ghosts[0] = getInky();
	ghosts[1] = getBlinky();
	ghosts[2] = getPinky();
	ghosts[3] = getClyde();
    */
    ghosts[0].cp_x = 8;//getInky();
	ghosts[0].cp_y = 15; 
	ghosts[1].cp_x = 14;//getBlinky();
	ghosts[1].cp_y = 9;
	ghosts[2].cp_x = 26; 
	ghosts[2].cp_y = 21;  //getPinky();
	ghosts[3].cp_x = 1;
	ghosts[3].cp_y = 1; //getClyde();
    int direc[4];
    direc[0] = 1;
    direc[1] = 1;
    direc[2] = 1;
    direc[3] = 1;
    uint8_t visited[868];
	clear_ghost_danger();
	for(int i=0; i<4; i++) {
        memset(&visited[0], 0, sizeof(uint8_t) * 868); 
		flood_node *head_fringe = (flood_node*) malloc(sizeof(flood_node));
        if (head_fringe == NULL) {
            printf("EOM. can't handle\n");
            exit(1);
        }

        /*int direc;
        if (i == 0)
            direc = direcs->ink_dir;
        else if (i == 1)
            direc = direcs->blink_dir;
        else if (i == 2)
            direc = direcs->pink_dir;
        else
            direc = direcs->clyde_dir;
        */
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

			add_legal_successors(cur_node->depth+1, cur_node->current_cell, &visited[0], &head_fringe, &tail, direc[i]);
            if (grid[28*cur_node->current_cell.coordinates.cp_x + cur_node->current_cell.coordinates.cp_y].ghost_danger > cur_node->depth) {
			    grid[28*cur_node->current_cell.coordinates.cp_x + cur_node->current_cell.coordinates.cp_y].ghost_danger = cur_node->depth; 
            }
            free(cur_node);
		}
	}
}

