def find_polyomino_power(h, w, grid):
    def dfs(x, y, color):
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if grid[cx][cy] == 'X':
                grid[cx][cy] = str(color)
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < h and 0 <= ny < w and grid[nx][ny] == 'X':
                        stack.append((nx, ny))

    def count_components():
        components = 0
        visited = [[False] * w for _ in range(h)]
        for i in range(h):
            for j in range(w):
                if grid[i][j] == 'X' and not visited[i][j]:
                    components += 1
                    dfs(i, j, components)
        return components

    def check_power(k):
        if k > 5:
            return False
        components = count_components()
        if components % k != 0:
            return False
        target_size = components // k
        for i in range(1, k + 1):
            count = sum(row.count(str(i)) for row in grid)
            if count != target_size:
                return False
        return True

    for k in range(2, 6):
        if check_power(k):
            return '\n'.join(''.join(row) for row in grid)
    return "No solution"

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
h = int(data[0])
w = int(data[1])
grid = data[2:]
result = find_polyomino_power(h, w, grid)
print(result)