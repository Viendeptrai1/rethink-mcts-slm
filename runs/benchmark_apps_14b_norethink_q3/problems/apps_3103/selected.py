MOD = 1000003

def count_paths(Y, X, x_init, map_data):
    # Initialize DP table
    dp = [[0] * X for _ in range(Y)]
    
    # Starting point
    dp[Y-1][x_init] = 1
    
    # Fill the DP table
    for y in range(Y-1, -1, -1):
        for x in range(X):
            if map_data[y][x] == '#':
                continue
            
            # Move north
            if y > 0:
                dp[y-1][x] = (dp[y-1][x] + dp[y][x]) % MOD
            
            # Move east
            if x < X-1 and map_data[y][x] != '<':
                dp[y][x+1] = (dp[y][x+1] + dp[y][x]) % MOD
            
            # Move west
            if x > 0 and map_data[y][x] != '>':
                dp[y][x-1] = (dp[y][x-1] + dp[y][x]) % MOD
    
    # Find the number of ways to reach the castle
    castle_x = map_data[0].index('@')
    return dp[0][castle_x]

# Read input
import sys
input = sys.stdin.read
data = input().split()

Y = int(data[0])
X = int(data[1])
x_init = int(data[2])
map_data = data[3:]

# Calculate and print the result
result = count_paths(Y, X, x_init, map_data)
print(result)