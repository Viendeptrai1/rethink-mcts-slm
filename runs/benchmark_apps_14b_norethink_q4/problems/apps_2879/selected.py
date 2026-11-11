import sys

def read_input():
    import sys
    input = sys.stdin.read
    data = input().split()
    h = int(data[0])
    w = int(data[1])
    grid = [data[2 + i * w:2 + (i + 1) * w] for i in range(h)]
    return h, w, grid

def is_power_polyomino(h, w, grid):
    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    def union(x, y):
        rootX = find(x)
        rootY = find(y)
        if rootX != rootY:
            parent[rootX] = rootY

    total_X = sum(row.count('X') for row in grid)
    if total_X == 0:
        return "No solution"
    
    for k in range(5, 1, -1):
        if total_X % k != 0:
            continue
        
        parent = list(range(h * w))
        size = [1] * (h * w)
        components = h * w
        
        for i in range(h):
            for j in range(w):
                if grid[i][j] == 'X':
                    idx = i * w + j
                    if i > 0 and grid[i - 1][j] == 'X':
                        union(idx, (i - 1) * w + j)
                    if j > 0 and grid[i][j - 1] == 'X':
                        union(idx, i * w + j - 1)
        
        for i in range(h):
            for j in range(w):
                if grid[i][j] == 'X':
                    idx = i * w + j
                    root = find(idx)
                    if size[root] > total_X // k:
                        break
            else:
                continue
            break
        else:
            result = [['.' for _ in range(w)] for _ in range(h)]
            component_map = {}
            next_num = 1
            for i in range(h):
                for j in range(w):
                    if grid[i][j] == 'X':
                        idx = i * w + j
                        root = find(idx)
                        if root not in component_map:
                            component_map[root] = next_num
                            next_num += 1
                        result[i][j] = str(component_map[root])
            return "\n".join("".join(row) for row in result)
    
    return "No solution"

def main():
    h, w, grid = read_input()
    print(is_power_polyomino(h, w, grid))

if __name__ == "__main__":
    main()