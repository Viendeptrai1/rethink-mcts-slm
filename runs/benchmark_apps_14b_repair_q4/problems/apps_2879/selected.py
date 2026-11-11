import sys
from collections import defaultdict

def find_polyomino_powers(h, w, grid):
    def get_neighbors(x, y):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w and grid[nx][ny] == 'X':
                yield nx, ny

    def dfs(x, y, component):
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if (cx, cy) not in component:
                component.add((cx, cy))
                for nx, ny in get_neighbors(cx, cy):
                    stack.append((nx, ny))

    components = []
    visited = set()
    for i in range(h):
        for j in range(w):
            if grid[i][j] == 'X' and (i, j) not in visited:
                component = set()
                dfs(i, j, component)
                components.append(component)
                visited.update(component)

    if len(components) == 1:
        component = components[0]
        size = len(component)
        for k in range(2, 6):
            if size % k == 0:
                sub_size = size // k
                sub_components = [set() for _ in range(k)]
                for (x, y) in component:
                    idx = (x * w + y) // sub_size
                    sub_components[idx].add((x, y))
                result = [['.' for _ in range(w)] for _ in range(h)]
                for idx, sub_component in enumerate(sub_components):
                    for (x, y) in sub_component:
                        result[x][y] = str(idx + 1)
                return '\n'.join(''.join(row) for row in result)
    return "No solution"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    h = int(data[0])
    w = int(data[1])
    grid = [data[2 + i * w:2 + (i + 1) * w] for i in range(h)]
    print(find_polyomino_powers(h, w, grid))

if __name__ == "__main__":
    main()