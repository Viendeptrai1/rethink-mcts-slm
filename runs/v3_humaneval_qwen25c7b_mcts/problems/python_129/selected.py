import heapq

def minPath(grid, k):
    n = len(grid)
    directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    
    pq = []
    for i in range(n):
        for j in range(n):
            heapq.heappush(pq, (grid[i][j], i, j, [grid[i][j]]))
    
    while pq:
        val, x, y, path = heapq.heappop(pq)
        
        if len(path) == k:
            return path
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n:
                heapq.heappush(pq, (val * 10 + grid[nx][ny], nx, ny, path + [grid[nx][ny]]))