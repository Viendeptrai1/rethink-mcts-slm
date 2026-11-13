import heapq

def minPath(grid, k):
    n = len(grid)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    def is_valid(x, y):
        return 0 <= x < n and 0 <= y < n
    
    # Priority queue to store paths, initialized with all starting points
    pq = []
    for i in range(n):
        for j in range(n):
            heapq.heappush(pq, (grid[i][j], [grid[i][j]]))
    
    while pq:
        current_value, path = heapq.heappop(pq)
        
        if len(path) == k:
            return path
        
        x, y = -1, -1
        for i in range(n):
            for j in range(n):
                if grid[i][j] == path[-1]:
                    x, y = i, j
                    break
            if x != -1:
                break
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                new_path = path + [grid[nx][ny]]
                heapq.heappush(pq, (new_path[-1], new_path))
    
    return []  # This line should never be reached if the problem guarantees a unique answer