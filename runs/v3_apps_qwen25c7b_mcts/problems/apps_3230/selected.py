import heapq
from math import sqrt

def min_explosions(R, C, grid):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    pq = []
    visited = set()
    
    # Initialize the priority queue with all 'X' positions
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'X':
                heapq.heappush(pq, (sqrt(r**2 + c**2), r, c))
    
    while pq:
        dist, x, y = heapq.heappop(pq)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        
        # Check all four possible directions
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < R and 0 <= ny < C and grid[nx][ny] == 'L':
                return 1
    
    return 0

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    R = int(data[0])
    C = int(data[1])
    grid = [data[i+2] for i in range(R)]
    print(min_explosions(R, C, grid))