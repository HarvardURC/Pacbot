#include "pacbot_direction.h"
#include "movement.h"

typedef struct directions{
	int direc;
	int* point;
} directions;

int pacbot_execute(uint8_t* start_array, int current_direction){
	if (start_array[0] == 0)
		return current_direction;
	if (start_array[0] != current_direction){
		return -1;
	}
	int i = 1;
	while(i < 200 && start_array[i] != 5){
		if (start_array[i] > 4 || start_array[i] < 0)
			break;
		if (start_array[i] == current_direction) {
			go_straight();
        }
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
        i++;
	}
	return current_direction;
}
