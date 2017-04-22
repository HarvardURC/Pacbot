#include "pacbot_direction.h"

typedef struct directions{
	int direc;
	int* point;
} directions;

int initial_direction = WEST;
int current_direction;
/*int pacbot_direction(){

	current_direction = initial_direction;

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
}*/

/*int pacbot_execute(uint8_t* start_array){
	//int cur_direction = pacbot_direction();
	if (start_array[0] == 0)
		return current_direction;
	if (start_array[0] != current_direction){
		return -1;
	}
	int i = 1;
	while(i < 200 && start_array[0] != 5){
		if (start_array[i] > 4 || start_array[i] < 0)
			break;
		if (start_array[i] == current_direction)
			go_straight();
		else if ((start_array[i] - current_direction) % 4 == 2 || (start_array[i] - current_direction) % 4 == -2){
			turn_around();
			go_straight();
		}
		else if ((start_array[i] - current_direction) % 4 == 3 || (start_array[i] - current_direction) % 4 == -1){
			turn_left();
			go_straight();
		}
		else if ((start_array[i] - current_direction) % 4 == 1 || (start_array[i] - current_direction) % 4 == -3){
			turn_right();
			go_straight();
		}
		current_direction = start_array[i];
	}
	return current_direction;
}*/