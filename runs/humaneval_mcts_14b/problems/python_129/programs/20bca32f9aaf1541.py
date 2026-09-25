def minPath(grid, k):
    import heapq
    
    N = len(grid)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    # Find the position of the smallest value in the grid
    min_value = float('inf')
    start_positions = []
    for i in range(N):
        for j in range(N):
            if grid[i][j] < min_value:
                min_value = grid[i][j]
                start_positions = [(i, j)]
            elif grid[i][j] == min_value:
                start_positions.append((i, j))
    
    # Priority queue to store paths, sorted by lexicographical order
    pq = []
    
    # Initialize the priority queue with all starting positions
    for x, y in start_positions:
        heapq.heappush(pq, ([grid[x][y]], x, y))
    
    # Perform BFS with priority queue
    while pq:
        path, x, y = heapq.heappop(pq)
        
        if len(path) == k:
            return path
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < N:
                new_path = path + [grid[nx][ny]]
                heapq.heappush(pq, (new_path, nx, ny))

# Example usage:
# grid = [[1,2,3], [4,5,6], [7,8,9]]
# k = 3
# print(minPath(grid, k))  # Output: [1, 2, 1]