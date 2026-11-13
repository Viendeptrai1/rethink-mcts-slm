import heapq

def minPath(grid, k):
    n = len(grid)
    directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    pq = []
    
    for i in range(n):
        for j in range(n):
            heapq.heappush(pq, (grid[i][j], i, j))
    
    while pq:
        value, x, y = heapq.heappop(pq)
        if k == 1:
            return [value]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n:
                heapq.heappush(pq, (value, nx, ny))
                
        k -= 1