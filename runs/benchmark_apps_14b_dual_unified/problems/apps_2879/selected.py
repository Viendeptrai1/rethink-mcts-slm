import sys

def read_input():
    import sys
    lines = sys.stdin.readlines()
    h, w = map(int, lines[0].split())
    grid = [list(line.strip()) for line in lines[1:h+1]]
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

def check_power(polyomino, k):
    h, w = len(polyomino), len(polyomino[0])
    for i in range(k):
        for x, y in polyomino:
            if x + i * h >= len(grid) or y + i * w >= len(grid[0]) or grid[x + i * h][y + i * w] != 'X':
                return False
    return True

def solve(h, w, grid):
    for polyomino in find_polyomino(grid):
        for k in range(2, 6):
            if check_power(polyomino, k):
                result = [['.' for _ in range(w)] for _ in range(h)]
                num = 1
                for i in range(k):
                    for x, y in polyomino:
                        result[x + i * h][y + i * w] = str(num)
                    num += 1
                for row in result:
                    print(''.join(row))
                return
    print("No solution")

if __name__ == "__main__":
    h, w, grid = read_input()
    solve(h, w, grid)