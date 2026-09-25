import heapq

def minPath(grid, k):
    N = len(grid)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    def bfs(start_row, start_col):
        min_path = None
        pq = []
        heapq.heappush(pq, (grid[start_row][start_col], [(start_row, start_col)]))
        
        while pq:
            current_value, path = heapq.heappop(pq)
            if len(path) == k:
                path_values = [grid[row][col] for row, col in path]
                if min_path is None or path_values < min_path:
                    min_path = path_values
                continue
            
            last_row, last_col = path[-1]
            for dr, dc in directions:
                new_row, new_col = last_row + dr, last_col + dc
                if 0 <= new_row < N and 0 <= new_col < N:
                    new_path = path + [(new_row, new_col)]
                    heapq.heappush(pq, (current_value + grid[new_row][new_col], new_path))
        
        return min_path
    
    overall_min_path = None
    for r in range(N):
        for c in range(N):
            path = bfs(r, c)
            if overall_min_path is None or path < overall_min_path:
                overall_min_path = path
    
    return overall_min_path

# Example usage:
# grid = [[1,2,3], [4,5,6], [7,8,9]]
# k = 3
# print(minPath(grid, k))  # Output: [1, 2, 1]