#ifndef _NETWORK_H_
#define _NETWORK_H_

#include <stdio.h> /* printf, sprintf */
#include <stdlib.h> /* exit */
#include <unistd.h> /* read, write, close */
#include <string.h> /* memcpy, memset */
#include <sys/socket.h> /* socket, connect */
#include <netinet/in.h> /* struct sockaddr_in, struct sockaddr */
#include <netdb.h> /* struct hostent, gethostbyname */

typedef enum {
    P_STOPPED,
    P_POWER,
    P_REGULAR
} game_status;

typedef struct cell_pos {
    int cp_x;
    int cp_y;
} cell_pos;

struct state_response {
    game_status sr_state; 
    cell_pos sr_pacbot;
    cell_pos sr_inky;
    cell_pos sr_blinky;
    cell_pos sr_pinky;
    cell_pos sr_clyde;
    int sr_power_counter;
};


int getState(struct state_response *state);
void printState(struct state_response *state);

#endif /* _NETWORK_H_*/
