#include "network.h"

#define NORTH 1
#define EAST 2
#define SOUTH 3
#define WEST 4

int pacbot_direction();
int pacbot_getnext(int* start);
void pacbot_execute(int);