#ifndef _DESIRED_COORDINATES_H_
#define _DESIRED_COORDINATES_H_

#include "state.h"
#include "desired_coordinates.h"

void desired_coordinates(cell_pos *max1, cell_pos *max2, cell_pos *max3);

int get_distance(cell_pos *a, cell_pos *b);

//returns length of a dirNode list
int dirNodeLength(dir_node* head);

//returns the action sequence required to move to the nearest ghost to pacbot
dir_node* frightAction();


#endif /* _DESIRED_COORDINATES_H_*/
