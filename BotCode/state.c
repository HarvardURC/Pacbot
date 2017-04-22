#include "state.h"

cell_pos getPacbot() {
    return latest_state->sr_pacbot;
}

cell_pos getClyde() {
    return latest_state->sr_clyde;
}

cell_pos getBlinky() {
    return latest_state->sr_blinky;
}

cell_pos getPinky() {
    return latest_state->sr_pinky;
}

cell_pos getInky() {
    return latest_state->sr_inky;
}

game_status getGameStatus() {
    return latest_state->sr_state;
}

int getPowerCoutner() {
    return latest_state->sr_power_counter;
}
