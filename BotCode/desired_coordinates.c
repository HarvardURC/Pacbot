#include <stdlib.h>
#include "grid.h"
// #include "movement.h"
#include "AStar.h"
#include "desired_coordinates.h"

void desired_coordinates(cell_pos *max1, cell_pos *max2, cell_pos *max3) {
	max1 = NULL;
	max2 = NULL;
	max3 = NULL;
	cell_pos pacbot = getPacbot();
	for (int i = 0; i < 868; i++){
		if (grid[i].food_opt == 'p'){
			if (get_distance(max1, &pacbot)  < get_distance(&grid[i].coordinates, &pacbot)){
				*max3 = *max2;
				*max2 = *max1;
				*max1 = grid[i].coordinates;
			}
			else if (get_distance(max2, &pacbot)  < get_distance(&grid[i].coordinates, &pacbot) && get_distance(&grid[i].coordinates, &pacbot)  < get_distance(max1, &pacbot) + 15){
				*max3 = *max2;
				*max2 = grid[i].coordinates;
			}
			else if (get_distance(max3, &pacbot) < get_distance(&grid[i].coordinates, &pacbot) && get_distance(&grid[i].coordinates, &pacbot) < get_distance(max2, &pacbot) + 7){
				*max3 = grid[i].coordinates;
			}
		}
	}
}

int get_distance(cell_pos *a, cell_pos *b) {
    if (a == NULL || b == NULL)  return -1;
	return abs(a->cp_x - b->cp_x) + abs (a->cp_y - b->cp_y);
}



//returns the action sequence required to move to the nearest ghost to pacbot
int frightAction() {
	//note new function wil be written that doesn't account ghost positions
	/*
    dir_node* ClydeAction = getActionList(getPacbot(), getClyde()); 
	dir_node* PinkyAction = getActionList(getPacbot(), getPinky());
	dir_node* InkyAction = getActionList(getPacbot(), getInky());
	dir_node* BlinkyAction = getActionList(getPacbot(), getBlinky());

	int maxlen = dirNodeLength(ClydeAction);
	dir_node* maxghost = ClydeAction; 

	if(dirNodeLength(PinkyAction) < maxlen){
		maxlen = dirNodeLength(PinkyAction);
		maxghost = PinkyAction;
	}
	else if(dirNodeLength(InkyAction) < maxlen){
		maxlen = dirNodeLength(InkyAction);
		maxghost = InkyAction;
	}
	else if(dirNodeLength(BlinkyAction) < maxlen){
		maxlen = dirNodeLength(BlinkyAction);
		maxghost = BlinkyAction;
	}
	return maxghost; 
    */
}

