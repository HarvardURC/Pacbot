#ifndef _PACBOT_DIRECTION_H_
#define _PACBOT_DIRECTION_H_

#include "network.h"

//int pacbot_direction();
int pacbot_getnext(int* start);
int pacbot_execute(uint8_t* start_array, int current_direction);

#endif /* _PACBOT_DIRECTION_H_*/
