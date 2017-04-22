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

typedef struct ghost_dir{
    int blink_dir;
    int ink_dir;
    int pink_dir;
    int clyde_dir;
} ghost_dir;

//food opt = pellet =1, big pellet =  2 ; empty= 3; fruit = 4
typedef struct free_cell {
    cell_pos coordinates; 
    int pacman_pos;
    int ghost_danger;
    char food_opt; 
 	cell_pos adj_cell[4]; 
    int directions[4]; 
} free_cell;

extern free_cell *grid; 
extern state_response *latest_state;

#define NORTH 	 1
#define EAST 	 2
#define SOUTH 	 3
#define WEST 	 4


cell_pos getPacbot();
cell_pos getClyde();
cell_pos getBlinky();
cell_pos getInky();
cell_pos getPinky();
game_status getGameStatus();
int getPowerCounter();




#endif /* _STATE_H_*/
