import sys
from collections import deque
import math

def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def bfs(grid, start_x, start_y):
    queue = deque([(start_x, start_y)])
    visited = set()
    visited.add((start_x, start_y))
    while queue:
        x, y = queue.popleft()
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 'L' and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))
    return len(visited)

def main():
    input = sys.stdin.read
    data = input().split()
    
    R = int(data[0])
    C = int(data[1])
    grid = []
    index = 2
    for i in range(R):
        row = list(data[index])
        grid.append(row)
        index += 1
    
    total_explosions = 0
    for i in range(R):
        for j in range(C):
            if grid[i][j] == 'X':
                neighbors = []
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < R and 0 <= nj < C and grid[ni][nj] == 'L':
                        neighbors.append((ni, nj))
                
                if neighbors:
                    min_distance = float('inf')
                    closest_seat = None
                    for neighbor in neighbors:
                        dist = euclidean_distance(i, j, neighbor[0], neighbor[1])
                        if dist < min_distance:
                            min_distance = dist
                            closest_seat = neighbor
                    
                    if closest_seat:
                        total_explosions += bfs(grid, closest_seat[0], closest_seat[1])
    
    print(total_explosions)

if __name__ == "__main__":
    main()