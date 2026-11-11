from typing import List

class Solution:
    def minPath(self, grid: List[List[int]], k: int) -> List[int]:
        N = len(grid)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        def dfs(x, y, path):
            if len(path) == k:
                return path
            
            min_path = None
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < N and 0 <= ny < N:
                    new_path = dfs(nx, ny, path + [grid[nx][ny]])
                    if min_path is None or new_path < min_path:
                        min_path = new_path
            return min_path
        
        min_result = None
        for i in range(N):
            for j in range(N):
                path = dfs(i, j, [grid[i][j]])
                if min_result is None or path < min_result:
                    min_result = path
        
        return min_result