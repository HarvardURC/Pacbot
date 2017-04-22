#include "grid.h"
#include "movement.h"
#include "desire_coordinates.h"
#include "state.h"
#include "AStar.h"

cell_pos desired_coordinates(cell_pos pacbot){
	cell_pos max1 = NULL;
	cell_pos max2 = NULL;
	cell_pos max3 = NULL;
	cell_pos temp = NULL;
	cell_pos pacbot = getPacbot();
	for (int i = 0; i < 868; i++){
		if (grid[i].food_opt == p){
			if (get_distance(max1, pacbot)  < get_distance(grid[i].coordinates, pacbot)){
				max3 = max2;
				max2 = max1;
				max1 = grid[i].coordinates;
			}
			else if (get_distance(max2, pacbot)  < get_distance(grid[i].coordinates, pacbot) && get_distance(grid[i].coordinates, pacbot)  < get_distance(max1, pacbot) + 15){
				max3 = max2;
				max2 = grid[i].coordinates;
			}
			else if (get_distance(max3, pacbot) < get_distance(grid[i].coordinates, pacbot) && get_distance(grid[i].coordinates, pacbot) < get_distance(max2, pacbot) + 7){
				max3 = grid[i].coordinates
			}
		}
	}
}

int get_distance(cell_pos a, cell_pos b) {
	int distance1 = abs (a.cp_x - b.cp_x) + abs (a.cp_y - b.cp_y);
	return distance1;
}


//returns length of a dirNode list
int dirNodeLength(struct dir_node* head){
	int length = 0;
	struct dir_node* track = head; 
	while (track != NULL)
	{
		length++;
		track = track->next; 
	}
	return length; 
}

//returns the action sequence required to move to the nearest ghost to pacbot
dir_node* frightAction(){
	//note new function wil be written that doesn't account ghost positions
	dir_node* ClydeAction = getActionList(getPacbot(), getClude()); 
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
}

