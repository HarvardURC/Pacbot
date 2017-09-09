#ifndef _DESIREDCOORDINATES_H_
#define _DESIREDCOORDINATES_H_

#include <stdio.h> /* printf, sprintf */
#include <stdlib.h> /* exit */
#include <unistd.h> /* read, write, close */
#include <string.h> /* memcpy, memset */
#include <sys/socket.h> /* socket, connect */
#include <netinet/in.h> /* struct sockaddr_in, struct sockaddr */
#include <netdb.h> /* struct hostent, gethostbyname */
#include "state.h"

void desired_coordinates(cell_pos *max1, cell_pos *max2, cell_pos *max3);
int get_distance(cell_pos *a, cell_pos *b);

#endif /* _NETWORK_H_*/
