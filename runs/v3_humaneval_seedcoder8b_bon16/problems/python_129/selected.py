def minPath(grid, k):
    from itertools import permutations
    
    n = len(grid)
    if k == 1:
        return [min(min(row) for row in grid)]
    
    # Generate all possible starting points in the grid
    starting_points = [(i, j) for i in range(n) for j in range(n)]
    
    def get_neighbors(x, y):
        # Possible moves: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n:
                neighbors.append((nx, ny))
        return neighbors
    
    min_path = None
    
    # Iterate over all possible starting points
    for start in starting_points:
        # BFS to find all paths of length k
        stack = [(start, [grid[start[0]][start[1]]])]
        while stack:
            (x, y), path = stack.pop()
            if len(path) == k:
                if min_path is None or path < min_path:
                    min_path = path
                continue
            for nx, ny in get_neighbors(x, y):
                stack.append(((nx, ny), path + [grid[nx][ny]]))
    
    return min_path