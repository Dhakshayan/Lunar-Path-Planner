import heapq

def a_star(grid, start, end):
    h, w = grid.shape
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, end), 0, start, [start]))
    visited = set()

    while open_set:
        _, cost, current, path = heapq.heappop(open_set)
        if current in visited:
            continue
        visited.add(current)

        if current == end:
            return path

        for neighbor in get_neighbors(current, h, w):
            if grid[neighbor] == 1 or neighbor in visited:
                continue
            new_cost = cost + 1
            priority = new_cost + heuristic(neighbor, end)
            heapq.heappush(open_set, (priority, new_cost, neighbor, path + [neighbor]))
    return None

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(pos, h, w):
    y, x = pos
    neighbors = []
    for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
        ny, nx = y + dy, x + dx
        if 0 <= ny < h and 0 <= nx < w:
            neighbors.append((ny, nx))
    return neighbors
