#include "state.h"

int temp;

cell_pos getPacbot() {
	temp = latest_state->sr_pacbot.cp_x;
	latest_state->sr_pacbot.cp_x = latest_state->sr_pacbot.cp_y;
	latest_state->sr_pacbot.cp_y = temp;
    return latest_state->sr_pacbot;
}

cell_pos getClyde() {
	temp = latest_state->sr_clyde.cp_x;
	latest_state->sr_clyde.cp_x = latest_state->sr_clyde.cp_y;
	latest_state->sr_clyde.cp_y = temp;
    return latest_state->sr_clyde;
}

cell_pos getBlinky() {
	temp = latest_state->sr_blinky.cp_x;
	latest_state->sr_blinky.cp_x = latest_state->sr_blinky.cp_y;
	latest_state->sr_blinky.cp_y = temp;
    return latest_state->sr_blinky;
}

cell_pos getPinky() {
	temp = latest_state->sr_pinky.cp_x;
	latest_state->sr_pinky.cp_x = latest_state->sr_pinky.cp_y;
	latest_state->sr_pinky.cp_y = temp;
    return latest_state->sr_pinky;
}

cell_pos getInky() {
	temp = latest_state->sr_inky.cp_x;
	latest_state->sr_inky.cp_x = latest_state->sr_inky.cp_y;
	latest_state->sr_inky.cp_y = temp;
    return latest_state->sr_inky;
}

game_status getGameStatus() {
    return latest_state->sr_state;
}

int getPowerCoutner() {
    return latest_state->sr_power_counter;
}
