MOD = 1000003

def count_paths(Y, X, x_init, grid):
    # Initialize the DP table
    dp = [[0] * X for _ in range(Y)]
    
    # Starting point
    dp[Y-1][x_init] = 1
    
    # Fill the DP table
    for y in range(Y-1, -1, -1):
        for x in range(X):
            if grid[y][x] == '#':
                continue
            if y + 1 < Y:
                dp[y][x] = (dp[y][x] + dp[y+1][x]) % MOD
            if grid[y][x] == '<' and x > 0:
                dp[y][x] = (dp[y][x] + dp[y][x-1]) % MOD
            if grid[y][x] == '>' and x + 1 < X:
                dp[y][x] = (dp[y][x] + dp[y][x+1]) % MOD
    
    # Find the number of ways to reach the castle
    castle_x = grid[0].index('@')
    return dp[0][castle_x]

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