#ifndef _PACBOT_DIRECTION_H_
#define _PACBOT_DIRECTION_H_

#include "network.h"

#define NORTH 1
#define EAST 2
#define SOUTH 3
#define WEST 4

int pacbot_direction();
int pacbot_getnext(int* start);
void pacbot_execute(int);

#endif /* _PACBOT_DIRECTION_H_*/
