from variables import *
import copy

def bfs(grid, state, targets):
    pac_loc = (state.pacman.x, state.pacman.y)
    visited = []
    queue = [(pac_loc, [])]

    while len(queue) > 0:
        nxt = queue.pop(0)
        visited.append(nxt[0])
        new_path = copy.deepcopy(nxt[1])
        new_path.append(nxt[0])
        loc = nxt[0]
        if grid[loc[0]][loc[1]] in targets:
            return new_path

        if grid[loc[0] + 1][loc[1]] in [o, e, O]:
            queue.append(((loc[0] + 1, loc[1]),new_path))
        if grid[loc[0] - 1][loc[1]] in [o, e, O]:
            queue.append(((loc[0] - 1, loc[1]),new_path))
        if grid[loc[0]][loc[1] + 1] in [o, e, O]:
            queue.append(((loc[0], loc[1] + 1),new_path))
        if grid[loc[0]][loc[1] - 1] in [o, e, O]:
            queue.append(((loc[0], loc[1] - 1),new_path))

    return None

