#include "AStar.h"
#include <math.h>
#include <stdlib.h>
#include "FloodFill.h"
#include <limits.h>
#include "grid.h"
#include <stdio.h>
#include "state.h"
//Add a node n to the end of current_node
void push_flood_node(flood_node* n, flood_node * current_node){ 
	if(n==NULL)
		return; 
	while(current_node->next_flood_node != NULL){
		current_node= current_node->next_flood_node; 
	}
	current_node->next_flood_node = n; 
	current_node = n; 
	current_node->next_flood_node = NULL; 
} 
//Returns the head node and moves head pointer to next node
free_cell pop_flood_node(flood_node* head){
	if(head == NULL)
		return head->current_cell; 
	free_cell cell = head->current_cell;

	if(head->next_flood_node == NULL)
		head =  NULL; 
	else
	head = head->next_flood_node;

	return cell;
}
//returns 0 if our list does not contain pos 1 if it does 
int  closed_contains(free_cell cell, flood_node * n){
	while(n->next_flood_node != NULL){
		if(cell.coordinates.cp_x == n->current_cell.coordinates.cp_x && cell.coordinates.cp_y == n->current_cell.coordinates.cp_y)
			return 1; 
		else 
			n = n->next_flood_node; 
	}
	return 0; 
}
//returns up to four possible next moves
flood_node * get_legal_successors(free_cell pos, int depth){
	flood_node * nodes_to_return = NULL; 	
	free_cell adjacent_cell; 
	for(int i=0; i<4; i++){
		adjacent_cell = grid[28*pos.adj_cell[i].cp_y +pos.adj_cell[i].cp_x];  
		if(adjacent_cell.ghost_danger > depth){
			adjacent_cell.ghost_danger = depth; 
		}
		if((adjacent_cell.food_opt != 'w') && (adjacent_cell.ghost_danger > pos.ghost_danger + 1)){
			flood_node * new_flood_node; 
			new_flood_node-> current_cell = adjacent_cell; 
			new_flood_node -> next_flood_node = NULL; 
			push_flood_node(new_flood_node, nodes_to_return); 
		}
	}
	return nodes_to_return; 
} 
void clear_ghost_danger(){
	for(int i=0; i<868; i++){
		grid[i].ghost_danger= INT_MAX; 
	}
}
// void print_linked_list(flood_node * head){
// 	flood_node * head_t = head; 
// 	while(head != NULL)
// 		printf("%d,%d\n", head->current_cell.coordinates.cp_x,head->current_cell.coordinates.cp_x);

// }
//on new ghost position update, change the main grid danger variable to match distance from ghosts
void ghost_flood(state_response state){
	cell_pos ghosts [4]; 
	ghosts[0] = state.sr_inky; 
	ghosts[1] = state.sr_blinky;
	ghosts[2] = state.sr_pinky;
	ghosts[3] = state.sr_clyde;
	clear_ghost_danger();
	for(int i=0; i<4; i++){
		flood_node * head_fringe;
		//flood_node * head_closed;
		flood_node * current_node; 
		grid[ghosts[i].cp_x + 28*ghosts[i].cp_y].ghost_danger = 0;
		current_node->current_cell = grid[ghosts[i].cp_x + 28*ghosts[i].cp_y];
		push_flood_node(current_node, head_fringe);
		int depth =1; 
		while (1){
			if(head_fringe == NULL){
				break; 
			}
			free_cell cell = pop_flood_node(head_fringe);
			flood_node * successors_head = get_legal_successors(cell, depth);
			if(successors_head!=NULL){
				push_flood_node(successors_head, head_fringe);
			}
			grid[cell.coordinates.cp_x + 28*cell.coordinates.cp_y].ghost_danger = depth; 
			depth = cell.ghost_danger +1;  
		}
		
	}
}

