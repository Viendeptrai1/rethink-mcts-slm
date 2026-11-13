import sys
from collections import deque

def min_quadcopter_path(x1, y1, x2, y2):
    queue = deque([(x1, y1, 0)])
    visited = set([(x1, y1)])
    
    while queue:
        x, y, steps = queue.popleft()
        
        if x == x1 and y == y1 and steps > 0:
            return steps
        
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            
            if (nx, ny) not in visited and min(nx, ny) >= -100 and max(nx, ny) <= 100:
                if not (x2 == x1 and y2 == y1 and x == x2 and y == y2):
                    if not (x2 == nx and y2 == ny):
                        queue.append((nx, ny, steps + 1))
                        visited.add((nx, ny))
    
    return -1  # No valid path found

if __name__ == "__main__":
    x1, y1 = map(int, input().split())
    x2, y2 = map(int, input().split())
    print(min_quadcopter_path(x1, y1, x2, y2))