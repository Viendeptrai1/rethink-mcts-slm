MOD = 1000003

def count_paths(Y, X, x_init, grid):
    # Initialize DP table
    dp = [[0] * X for _ in range(Y)]
    dp[Y-1][x_init] = 1
    
    # Fill DP table
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
    
    # Find the castle position
    for y in range(Y):
        for x in range(X):
            if grid[y][x] == '@':
                return dp[y][x]
    
    return "begin repairs"

# Read input
import sys
input = sys.stdin.read
data = input().split()

Y = int(data[0])
X = int(data[1])
x_init = int(data[2])
grid = data[3:]

# Output the result
print(count_paths(Y, X, x_init, grid))