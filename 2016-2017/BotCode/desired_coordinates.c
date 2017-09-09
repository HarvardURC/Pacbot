#include <stdlib.h>
#include "grid.h"
#include "movement.h"
#include "AStar.h"
#include "desired_coordinates.h"

void desired_coordinates(cell_pos *max1, cell_pos *max2, cell_pos *max3) {
	cell_pos cur_max1;
	cell_pos cur_max2;
	cell_pos cur_max3;
	cur_max1.cp_x = -1;
	cur_max1.cp_y = -1;
	cur_max2.cp_x = -1;
	cur_max2.cp_y = -1;
	cur_max3.cp_x = -1;
	cur_max3.cp_y = -1;
	cell_pos pacbot = getPacbot();
    int i;
	for (i = 0; i < 868; i++){
		if (grid[i].food_opt == 'p'){
			if (get_distance(&cur_max1, &pacbot)  < get_distance(&grid[i].coordinates, &pacbot) &&
                    get_distance(&grid[i].coordinates, &pacbot) < 15){
				cur_max3 = cur_max2;
				cur_max2 = cur_max1;
				cur_max1 = grid[i].coordinates;
			}
			else if (get_distance(&cur_max2, &pacbot)  < get_distance(&grid[i].coordinates, &pacbot) &&
				    get_distance(&cur_max1, &grid[i].coordinates) > 10 &&
                    (cur_max3.cp_x == -1 || get_distance(&cur_max3, &grid[i].coordinates) > 10) &&
                    get_distance(&grid[i].coordinates, &pacbot) < 15){
				cur_max3 = cur_max2;
				cur_max2 = grid[i].coordinates;
			}
			else if (get_distance(&cur_max3, &pacbot) < get_distance(&grid[i].coordinates, &pacbot) &&
				get_distance(&cur_max2, &grid[i].coordinates) > 7 &&
                get_distance(&cur_max1, &grid[i].coordinates) > 7 &&
                get_distance(&grid[i].coordinates, &pacbot) < 15){
				cur_max3 = grid[i].coordinates;
			}
		}
	}
    if (cur_max1.cp_x != -1) {
        *max1 = cur_max1;
    } else {
        max1->cp_x = 111;
    }
    if (cur_max2.cp_x != -1) {
        *max2 = cur_max2;
    } else {
        max2->cp_x = 111;
    }
    if (cur_max3.cp_x != -1) {
        *max3 = cur_max3;
    } else {
        max3->cp_x = 111;
    }
}

int get_distance(cell_pos *a, cell_pos *b) {
    if (a == NULL || b == NULL || a->cp_x == -1 || b->cp_x == -1) {
        return -1;
    }
	int dist = abs(a->cp_x - b->cp_x) + abs (a->cp_y - b->cp_y);
    return dist;
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

