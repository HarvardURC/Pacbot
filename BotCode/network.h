#ifndef _NETWORK_H_
#define _NETWORK_H_

#include <stdio.h> /* printf, sprintf */
#include <stdlib.h> /* exit */
#include <unistd.h> /* read, write, close */
#include <string.h> /* memcpy, memset */
#include <sys/socket.h> /* socket, connect */
#include <netinet/in.h> /* struct sockaddr_in, struct sockaddr */
#include <netdb.h> /* struct hostent, gethostbyname */
#include "state.h"

void pollState();
int getState(state_response *state);
void printState(state_response *state);

#endif /* _NETWORK_H_*/
