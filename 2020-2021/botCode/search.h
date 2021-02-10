#ifndef BFS_SEARCH_H
#define BFS_SEARCH_H
#include "variables.h"
#include <vector>

extern std::vector<Coord> bfs(int *grid[], Coord start, Coord target);

extern std::vector<Coord> bfs(int *grid[], Coord start, std::vector<int> target);

extern std::vector<Coord> bfs(int *grid[], Coord start, Coord target, int max_dist);

extern std::vector<Coord> bfs(int *grid[], Coord start, std::vector<int> target, int max_dist);
#endif