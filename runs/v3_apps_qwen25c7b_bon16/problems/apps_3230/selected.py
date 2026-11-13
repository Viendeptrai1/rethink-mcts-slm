import sys
from collections import deque
import math

def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def bfs(grid, start):
    queue = deque([start])
    visited = set()
    visited.add(start)
    while queue:
        x, y = queue.popleft()
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != '.' and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))
    return visited

def count_explosions(grid):
    rows, cols = len(grid), len(grid[0])
    rudeness_points = [(i, j) for i in range(rows) for j in range(cols) if grid[i][j] == 'X']
    seats = [(i, j) for i in range(rows) for j in range(cols) if grid[i][j] == 'L']

    explosions = 0
    while rudeness_points:
        min_distance = float('inf')
        target_seat = None
        for seat in seats:
            distance = min(euclidean_distance(seat[0], seat[1], rx, ry) for rx, ry in rudeness_points)
            if distance < min_distance:
                min_distance = distance
                target_seat = seat
            elif distance == min_distance and abs(target_seat[0] - seat[0]) + abs(target_seat[1] - seat[1]) > abs(seat[0] - rx) + abs(seat[1] - ry):
                target_seat = seat

        if not target_seat:
            break

        rudeness_set = bfs(grid, target_seat)
        rudeness_points = [point for point in rudeness_points if point not in rudeness_set]
        seats.remove(target_seat)
        explosions += 1

    return explosions

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().splitlines()
    r, c = map(int, data[0].split())
    grid = data[1:]

    result = count_explosions(grid)
    print(result)