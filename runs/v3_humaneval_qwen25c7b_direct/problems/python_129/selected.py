from heapq import heappop, heappush

class Solution:
    def minPath(self, grid, k):
        N = len(grid)
        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        heap = []
        visited = set()
        
        for i in range(N):
            for j in range(N):
                heappush(heap, (grid[i][j], i, j))
        
        while heap:
            val, x, y = heappop(heap)
            if (x, y) in visited:
                continue
            visited.add((x, y))
            if len(visited) == k:
                return [grid[x][y] for x, y in sorted(list(visited))]
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < N and 0 <= ny < N:
                    heappush(heap, (grid[nx][ny], nx, ny))

# Example usage:
solution = Solution()
print(solution.minPath([[1,2,3],[4,5,6],[7,8,9]], 3))  # Output: [1, 2, 1]
print(solution.minPath([[5,9,3],[4,1,6],[7,8,2]], 1))  # Output: [1]