import heapq

def minPath(grid, k):
    N = len(grid)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    # Priority queue to store paths, sorted by lexicographical order
    pq = []
    
    # Initialize the priority queue with all starting positions
    for i in range(N):
        for j in range(N):
            heapq.heappush(pq, ([grid[i][j]], i, j))
    
    # Explore paths
    while pq:
        path, x, y = heapq.heappop(pq)
        
        # If the path length is k, return the path
        if len(path) == k:
            return path
        
        # Expand the current path by moving to neighboring cells
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < N:
                new_path = path + [grid[nx][ny]]
                heapq.heappush(pq, (new_path, nx, ny))

# Example usage:
# grid = [[1,2,3], [4,5,6], [7,8,9]]
# k = 3
# print(minPath(grid, k))  # Output: [1, 2, 1]