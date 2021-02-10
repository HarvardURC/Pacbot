#ifndef MY_GLOBALS_H
#define MY_GLOBALS_H
#include <vector>

Coord pacbot_starting_pos = Coord(14, 7);

extern int I;
extern int o;
extern int e;
extern int O;
extern int n;

extern std::vector<int> not_wall_chars;

extern int **base_grid;

struct Coord
{
    int x;
    int y;

    Coord()
    {
        x = -1;
        y = -1;
    }

    Coord(int x_c, int y_c)
    {
        x = x_c;
        y = y_c;
    }

    bool operator==(const Coord &other)
    {
        return (x == other.x) && (y == other.y);
    }
};

#endif
