from variables import *
import copy

def bfs(grid, start, target, max_dist=float("inf")):
    visited = []
    queue = [(start, [])]

    while len(queue) > 0:
        nxt = queue.pop(0)
        visited.append(nxt[0])
        new_path = copy.deepcopy(nxt[1])
        new_path.append(nxt[0])
        loc = nxt[0]
        if type(target) is tuple:
            if target == loc:
                return new_path
        elif grid[loc[0]][loc[1]] in target:
            return new_path

        if grid[loc[0] + 1][loc[1]] in [o, e, O] and (loc[0] + 1, loc[1]) not in visited and len(new_path) <= max_dist:
            queue.append(((loc[0] + 1, loc[1]),new_path))
        if grid[loc[0] - 1][loc[1]] in [o, e, O] and (loc[0] - 1, loc[1]) not in visited and len(new_path) <= max_dist:
            queue.append(((loc[0] - 1, loc[1]),new_path))
        if grid[loc[0]][loc[1] + 1] in [o, e, O] and (loc[0], loc[1] + 1) not in visited and len(new_path) <= max_dist:
            queue.append(((loc[0], loc[1] + 1),new_path))
        if grid[loc[0]][loc[1] - 1] in [o, e, O] and (loc[0], loc[1] - 1) not in visited and len(new_path) <= max_dist:
            queue.append(((loc[0], loc[1] - 1),new_path))

    return None
