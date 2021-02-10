#include "search.h"
#include "variables.h"

const int ADDRESS = 69;
const int PORT = 420;

const int FREQUENCY = 30;
const float PELLET_WEIGHT = 0.65;
const float GHOST_WEIGHT = 0.35;
const float FRIGHTENED_GHOST_WEIGHT = .3 * GHOST_WEIGHT;
const int GHOST_CUTOFF = 10;

class HeuristicHighLevelModule
{
private:
    int subscriptions[];
    int state;
    Coord previous_loc;
    int direction;
    int **grid;

public:
    HeuristicHighLevelModule(int addr, int port)
    {
        grid = base_grid;
    }
    bool is_power_pellet_closer(std::vector<int> path)
    {
        std::vector<int>::iterator it;
        it = std::find(path.begin(), path.end(), O);
        return it != path.end();
    }
    bool find_distance_of_closest_pellet(Coord target_loc)
    {
        return bfs(grid, target_loc, std::vector<int>{o}).size - 1;
    }
    bool target_is_invalid(Coord target_loc)
    {
        std::vector<int>::iterator int_it;
        int_it = std::find(not_wall_chars.begin(), not_wall_chars.end(), grid[target_loc.x][target_loc.y]);
        return int_it == not_wall_chars.end();
    }
};