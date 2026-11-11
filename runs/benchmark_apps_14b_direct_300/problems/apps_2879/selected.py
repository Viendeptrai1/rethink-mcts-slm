import sys
from collections import defaultdict

def read_input():
    import sys
    data = sys.stdin.read().splitlines()
    h, w = map(int, data[0].split())
    grid = [list(line) for line in data[1:h+1]]
    return h, w, grid

def find_polyomino(grid, h, w):
    visited = [[False] * w for _ in range(h)]
    polyominoes = []
    
    def dfs(x, y, polyomino):
        if x < 0 or x >= h or y < 0 or y >= w or visited[x][y] or grid[x][y] == '.':
            return
        visited[x][y] = True
        polyomino.append((x, y))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            dfs(x + dx, y + dy, polyomino)
    
    for i in range(h):
        for j in range(w):
            if grid[i][j] == 'X' and not visited[i][j]:
                polyomino = []
                dfs(i, j, polyomino)
                polyominoes.append(polyomino)
    
    return polyominoes

def is_power(polyomino, k):
    if len(polyomino) % k != 0:
        return False
    
    part_size = len(polyomino) // k
    parts = [polyomino[i:i + part_size] for i in range(0, len(polyomino), part_size)]
    
    def shift(part, dx, dy):
        return [(x + dx, y + dy) for x, y in part]
    
    def can_place(part, grid, h, w):
        for x, y in part:
            if x < 0 or x >= h or y < 0 or y >= w or grid[x][y] != '.':
                return False
        return True
    
    def place_part(part, grid, num):
        for x, y in part:
            grid[x][y] = str(num)
    
    def remove_part(part, grid):
        for x, y in part:
            grid[x][y] = '.'
    
    def backtrack(parts, grid, num):
        if num == k + 1:
            return True
        for part in parts:
            for dx in range(-h, h):
                for dy in range(-w, w):
                    shifted_part = shift(part, dx, dy)
                    if can_place(shifted_part, grid, h, w):
                        place_part(shifted_part, grid, num)
                        if backtrack(parts[:parts.index(part)] + parts[parts.index(part) + 1:], grid, num + 1):
                            return True
                        remove_part(shifted_part, grid)
        return False
    
    empty_grid = [['.' for _ in range(w)] for _ in range(h)]
    return backtrack(parts, empty_grid, 1)

def main():
    h, w, grid = read_input()
    polyominoes = find_polyomino(grid, h, w)
    
    for k in range(2, 6):
        if all(is_power(polyomino, k) for polyomino in polyominoes):
            for polyomino in polyominoes:
                for x, y in polyomino:
                    grid[x][y] = str(k)
            for row in grid:
                print(''.join(row))
            return
    
    print("No solution")

if __name__ == "__main__":
    main()