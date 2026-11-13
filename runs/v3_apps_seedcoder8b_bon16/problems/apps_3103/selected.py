from collections import deque
import sys
input = sys.stdin.read

MOD = 1000003

def count_routes(Y, X, x_init, grid):
    directions = [(-1, 0), (0, -1), (0, 1)]  # Move north, west, east
    dp = [[0] * X for _ in range(Y)]
    
    # Find the position of the castle
    castle_x, castle_y = None, None
    for y in range(Y):
        for x in range(X):
            if grid[y][x] == '@':
                castle_x, castle_y = x, y
                break
        if castle_x is not None:
            break
    
    # Initialize the starting point
    dp[Y-1][x_init] = 1
    
    # BFS to populate the DP table
    queue = deque([(Y-1, x_init)])
    while queue:
        y, x = queue.popleft()
        
        # Try moving in all possible directions
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            
            if 0 <= ny < Y and 0 <= nx < X and grid[ny][nx] != '#':
                if grid[ny][nx] in ('~', '>') and dp[ny][nx] == 0:
                    queue.append((ny, nx))
                
                if grid[ny][nx] == '<' and x - 1 >= 0 and grid[y][x-1] == '<' and dp[ny][nx] == 0:
                    queue.append((ny, nx))
                
                dp[ny][nx] = (dp[ny][nx] + dp[y][x]) % MOD
    
    return dp[castle_y][castle_x] if dp[castle_y][castle_x] > 0 else "begin repairs"

def main():
    data = input().strip().split('\n')
    Y, X, x_init = map(int, data[0].split())
    grid = [data[i+1] for i in range(Y)]
    
    result = count_routes(Y, X, x_init, grid)
    print(result)

if __name__ == "__main__":
    main()