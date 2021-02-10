#include "search.h"
#include "variables.h"
#include <vector>

// BFSCoord
// A struct which stores a location on the board and its distance from
// the starting position of the breadth first search.
struct BFSCoord
{
    // the x and y coordinates of the location on the grid
    int x;
    int y;
    // the distance from the starting position of the breadth first search
    int dist;

    BFSCoord(int x_c, int y_c, int dist_c)
    {
        x = x_c;
        y = y_c;
        dist = dist_c;
    }

    BFSCoord(Coord coord, int dist_c)
    {
        x = coord.x;
        y = coord.y;
        dist = dist_c;
    }

    bool operator==(const Coord &other)
    {
        return (x == other.x) && (y == other.y);
    }
    bool operator==(const BFSCoord &other)
    {
        return (x == other.x) && (y == other.y);
    }
};

std::vector<int>::iterator find(int i, std::vector<int> vec)
{
    std::vector<int>::iterator it;
    it = std::find(vec.begin(), vec.end(), i);
    return it;
}

std::vector<BFSCoord>::iterator find(Coord coords, std::vector<BFSCoord> vec)
{
    std::vector<BFSCoord>::iterator it;
    it = std::find(vec.begin(), vec.end(), coords);
    return it;
}

std::vector<BFSCoord>::iterator find(BFSCoord coords, std::vector<BFSCoord> vec)
{
    std::vector<BFSCoord>::iterator it;
    it = std::find(vec.begin(), vec.end(), coords);
    return it;
}

// default distance from start to seach is effectively infinite
std::vector<Coord> bfs(int *grid[], Coord start, Coord target)
{
    return bfs(grid, start, target, __INT_MAX__);
}

std::vector<Coord> bfs(int *grid[], Coord start, std::vector<int> target)
{
    return bfs(grid, start, target, __INT_MAX__);
}

std::vector<Coord> bfs(int *grid[], Coord start, Coord target, int max_dist)
{
    if (start == target)
    {
        return {};
    }

    BFSCoord bfs_start = BFSCoord(start, 0);
    std::vector<BFSCoord> visited = {};
    std::vector<BFSCoord> to_visit = {bfs_start};

    while (to_visit.size > 0)
    {
        // checks most recently added coordinate pair
        BFSCoord cur = to_visit.back();
        to_visit.pop_back();

        if (cur.dist == max_dist)
        {
            return {};
        }

        for (int x_off = -1; x_off <= 1; x_off++)
        {
            for (int y_off = -1; y_off <= 1; y_off++)
            {
                // does not check spaces diagonally adjacent to cur
                if (x_off != y_off && x_off != 2 - y_off)
                {
                    BFSCoord next_loc = BFSCoord(cur.x + x_off, cur.y + y_off, cur.dist + 1);

                    // backtraces from end of path to beginning
                    if (next_loc == target)
                    {
                        std::vector<Coord> path = {target};
                        Coord pathstep = Coord(cur.x, cur.y);
                        path.insert(path.begin(), pathstep);

                        while (cur.dist != 0)
                        {
                            for (int i = -1; i <= 1; i++)
                            {
                                for (int j = -1; j <= 1; j++)
                                {
                                    // does not check spaces diagonally adjacent to cur
                                    if (x_off != y_off && x_off != 2 - y_off)
                                    {
                                        Coord adj_loc = Coord(cur.x + i, cur.y + j);

                                        std::vector<BFSCoord>::iterator coord_it = find(adj_loc, visited);
                                        // is this supposed to be != or ==
                                        if (coord_it != visited.end() && (*coord_it).dist == cur.dist - 1)
                                        {
                                            path.insert(path.begin(), adj_loc);
                                            cur = *coord_it;
                                            i = 2;
                                            j = 2;
                                        }
                                    }
                                }
                            }
                        }
                        return path;
                    }

                    // only will visit next_loc if next_loc isn't a wall and hasn't been visited
                    std::vector<int>::iterator int_it = find(grid[next_loc.x][next_loc.y], not_wall_chars);
                    if (int_it == not_wall_chars.end())
                    {
                        continue;
                    }
                    std::vector<BFSCoord>::iterator coord_it = find(next_loc, visited);
                    if (coord_it == visited.end())
                    {
                        continue;
                    }

                    to_visit.push_back(next_loc);
                }
            }
        }
    }
}

std::vector<Coord> bfs(int *grid[], Coord start, std::vector<int> target, int max_dist)
{
    std::vector<int>::iterator it = find(grid[start.x][start.y], target);
    if (it != target.end())
    {
        return {};
    }

    BFSCoord bfs_start = BFSCoord(start, 0);
    std::vector<BFSCoord> visited = {};
    std::vector<BFSCoord> to_visit = {bfs_start};

    while (to_visit.size > 0)
    {
        // backtraces from end of path to beginning
        BFSCoord cur = to_visit.back();
        to_visit.pop_back();

        if (cur.dist == max_dist)
        {
            return {};
        }

        for (int x_off = -1; x_off <= 1; x_off++)
        {
            for (int y_off = -1; y_off <= 1; y_off++)
            {
                // does not check spaces diagonally adjacent to cur
                if (x_off != y_off && x_off != 2 - y_off)
                {
                    BFSCoord next_loc = BFSCoord(cur.x + x_off, cur.y + y_off, cur.dist + 1);
                    std::vector<int>::iterator it = find(grid[next_loc.x][next_loc.y], target);
                    // backtraces from end of path to beginning if next_loc is a target
                    if (it != target.end())
                    {
                        std::vector<Coord> path = {Coord(next_loc.x, next_loc.y)};
                        Coord pathstep = Coord(cur.x, cur.y);
                        path.insert(path.begin(), pathstep);

                        while (cur.dist != 0)
                        {
                            for (int i = -1; i <= 1; i++)
                            {
                                for (int j = -1; j <= 1; j++)
                                {
                                    // does not check spaces diagonally adjacent to cur
                                    if (x_off != y_off && x_off != 2 - y_off)
                                    {
                                        Coord adj_loc = Coord(cur.x + i, cur.y + j);

                                        std::vector<BFSCoord>::iterator coord_it = find(adj_loc, visited);
                                        // is this supposed to be != or ==
                                        if (coord_it != visited.end() && (*coord_it).dist == cur.dist - 1)
                                        {
                                            path.insert(path.begin(), adj_loc);
                                            cur = *coord_it;
                                            i = 2;
                                            j = 2;
                                        }
                                    }
                                }
                            }
                        }
                        return path;
                    }

                    // only will visit next_loc if next_loc isn't a wall and hasn't been visited
                    std::vector<int>::iterator int_it = find(grid[next_loc.x][next_loc.y], not_wall_chars);
                    if (int_it == not_wall_chars.end())
                    {
                        continue;
                    }
                    std::vector<BFSCoord>::iterator coord_it = find(next_loc, visited);
                    if (coord_it == visited.end())
                    {
                        continue;
                    }

                    to_visit.push_back(next_loc);
                }
            }
        }
    }
}