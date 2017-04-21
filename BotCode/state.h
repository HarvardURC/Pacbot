#ifndef _STATE_H_
#define _STATE_H_

typedef enum {
    P_STOPPED,
    P_POWER,
    P_REGULAR
} game_status;

typedef struct cell_pos {
    int cp_x;
    int cp_y;
} cell_pos;

typedef struct state_response {
    game_status sr_state; 
    cell_pos sr_pacbot;
    cell_pos sr_inky;
    cell_pos sr_blinky;
    cell_pos sr_pinky;
    cell_pos sr_clyde;
    int sr_power_counter;
} state_response;

typedef struct game_state {
	cell_pos cur_pos; 
	int dir; 
} game_state;

typedef struct free_cell {
    cell_pos coordinates; 
    int pacman_pos;
    int ghost_danger;
    char food_opt; 
 	cell_pos adj_cell[4]; 
    int directions[4]; 
} free_cell;

extern free_cell *grid; 

#define NORTH 	 1;
#define EAST 	 2;
#define SOUTH 	 3;
#define WEST 	 4;


#endif /* _STATE_H_*/
