import sys
from collections import defaultdict

def read_input():
    import sys
    data = sys.stdin.read().splitlines()
    h, w = map(int, data[0].split())
    grid = [list(line) for line in data[1:]]
    return h, w, grid

def find_polyomino(grid):
    h, w = len(grid), len(grid[0])
    visited = [[False] * w for _ in range(h)]
    polyomino = []

    def dfs(x, y):
        if x < 0 or x >= h or y < 0 or y >= w or visited[x][y] or grid[x][y] == '.':
            return
        visited[x][y] = True
        polyomino.append((x, y))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            dfs(x + dx, y + dy)

    for i in range(h):
        for j in range(w):
            if grid[i][j] == 'X' and not visited[i][j]:
                polyomino.clear()
                dfs(i, j)
                yield polyomino

def is_power(polyomino, k):
    if len(polyomino) % k != 0:
        return False
    part_size = len(polyomino) // k
    parts = [polyomino[i:i + part_size] for i in range(0, len(polyomino), part_size)]
    for i in range(k):
        for j in range(i + 1, k):
            if any(abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) > 1 for p1, p2 in zip(parts[i], parts[j])):
                return False
    return True

def solve(h, w, grid):
    for polyomino in find_polyomino(grid):
        for k in range(2, 6):
            if is_power(polyomino, k):
                result = [['.' for _ in range(w)] for _ in range(h)]
                part_size = len(polyomino) // k
                for i in range(k):
                    for j in range(part_size):
                        x, y = polyomino[i * part_size + j]
                        result[x][y] = str(i + 1)
                return '\n'.join(''.join(row) for row in result)
    return "No solution"

if __name__ == "__main__":
    h, w, grid = read_input()
    print(solve(h, w, grid))