MOD = 1000003

def count_paths(Y, X, x_init, grid):
    dp = [[0] * X for _ in range(Y)]
    dp[-1][x_init] = 1
    
    def in_bounds(x, y):
        return 0 <= x < X and 0 <= y < Y
    
    for y in range(Y-2, -1, -1):
        for x in range(X):
            if grid[y][x] == '#':
                continue
            if grid[y][x] == '@':
                dp[y][x] = 1
                continue
            if grid[y][x] == '~':
                if in_bounds(x, y + 1):
                    dp[y][x] += dp[y + 1][x]
            elif grid[y][x] == '>':
                if in_bounds(x + 1, y) and grid[y][x + 1] != '<' and grid[y][x + 1] != '#':
                    dp[y][x] += dp[y][x + 1]
                if in_bounds(x, y + 1):
                    dp[y][x] += dp[y + 1][x]
            elif grid[y][x] == '<':
                if in_bounds(x - 1, y) and grid[y][x - 1] != '>' and grid[y][x - 1] != '#':
                    dp[y][x] += dp[y][x - 1]
                if in_bounds(x, y + 1):
                    dp[y][x] += dp[y + 1][x]
    
    return sum(dp[0]) % MOD

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    Y = int(data[0])
    X = int(data[1])
    x_init = int(data[2])
    grid = [data[i + 3] for i in range(Y)]
    result = count_paths(Y, X, x_init, grid)
    if result == 0:
        print("begin repairs")
    else:
        print(result)