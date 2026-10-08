MOD = 1000003

def count_paths(Y, X, x_init, grid):
    def dfs(y, x, visited):
        if y == 0 and grid[y][x] == '@':
            return 1
        if (y, x) in visited:
            return 0
        visited.add((y, x))
        paths = 0
        # Move north
        if y > 0 and grid[y-1][x] != '#':
            paths = (paths + dfs(y-1, x, visited)) % MOD
        # Move east
        if x + 1 < X and grid[y][x+1] != '#' and grid[y][x+1] != '<':
            paths = (paths + dfs(y, x+1, visited)) % MOD
        # Move west
        if x > 0 and grid[y][x-1] != '#' and grid[y][x-1] != '>':
            paths = (paths + dfs(y, x-1, visited)) % MOD
        visited.remove((y, x))
        return paths

    return dfs(Y-1, x_init, set())

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    Y = int(data[0])
    X = int(data[1])
    x_init = int(data[2])
    
    grid = []
    index = 3
    for _ in range(Y):
        grid.append(data[index])
        index += 1
    
    result = count_paths(Y, X, x_init, grid)
    if result == 0:
        print("begin repairs")
    else:
        print(result)

if __name__ == "__main__":
    main()