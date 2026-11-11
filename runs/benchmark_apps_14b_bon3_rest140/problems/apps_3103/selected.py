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
            if y + 1 < Y and grid[y+1][x] != '#':
                dp[y][x] = (dp[y][x] + dp[y+1][x]) % MOD
            if grid[y][x] == '<' and x > 0 and grid[y][x-1] != '#' and grid[y][x-1] != '>':
                dp[y][x] = (dp[y][x] + dp[y][x-1]) % MOD
            if grid[y][x] == '>' and x + 1 < X and grid[y][x+1] != '#' and grid[y][x+1] != '<':
                dp[y][x] = (dp[y][x] + dp[y][x+1]) % MOD
    
    # Find the number of ways to reach the castle
    castle_x = grid[0].index('@')
    return dp[0][castle_x]

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