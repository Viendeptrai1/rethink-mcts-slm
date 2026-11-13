import sys
import math
from collections import deque

def count_explosions(R, C, grid):
    def euclidean_distance(x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def find_nearest_seat(x, y):
        min_distance = float('inf')
        seat = None
        for i in range(R):
            for j in range(C):
                if grid[i][j] == 'L':
                    distance = euclidean_distance(x, y, i, j)
                    if distance < min_distance:
                        min_distance = distance
                        seat = (i, j)
        return seat

    def bfs():
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        queue = deque()
        for i in range(R):
            for j in range(C):
                if grid[i][j] == 'X':
                    queue.append((i, j))

        explosions = 0
        seated = set()

        while queue:
            x, y = queue.popleft()
            if (x, y) in seated:
                continue

            seat = find_nearest_seat(x, y)
            if seat is None:
                return explosions

            sx, sy = seat
            if grid[sx][sy] == 'L':
                grid[sx][sy] = 'X'
                seated.add((sx, sy))
            else:
                explosions += 1

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < R and 0 <= ny < C and grid[nx][ny] == 'X' and (nx, ny) not in seated:
                    queue.append((nx, ny))

        return explosions

    return bfs()

def main():
    input = sys.stdin.read
    data = input().splitlines()
    R, C = map(int, data[0].split())
    grid = [list(data[i + 1]) for i in range(R)]
    result = count_explosions(R, C, grid)
    print(result)

if __name__ == "__main__":
    main()