#include "pacbot_direction.h"

typedef struct directions{
	int direc;
	int* point;
} directions;

int pacbot_direction(){

	int direction;

	state_response state = NULL;
	get_state(*state);

	cell_pos pacbot_current;
	poll_state();
	cell_pos pacbot_init = getPacbot();

	while (pacbot_current = getPacbot() == pacbot_init){};

	poll_state();

	grid[pacbot_current.cp_x + 28*pacbot_current.]
	if (pacbot_current.cp_x != pacbot_init.cp_x){
		if (pacbot_current.cp_x < pacbot_init.cp_x)
			direction = WEST;
		else
			direction = EAST;
	}
	else{
		if (pacbot_current.cp_y < pacbot_init.cp_y)
			direction = NORTH;
		else
			direction = SOUTH
	}

	return direction;
}

int pacbot_getnext(start){
	directions next_direc = *start;
	while(next_direc.point != NULL){
		pacbot_execute(next_direc.direc);
		next_direc = *next_direc.point;
	}
	return 1;
}

void pacbot_execute(command){
	int cur_direction = pacbot_direction();
	if ((command - cur_direction) % 4 == 2)
		turn_around();
	else if ((command - cur_direction) % 4 == 3)
		turn_left();
	else if ((command - cur_direction) % 4 == 1)
		turn_right();
	else
		go_straight();
}