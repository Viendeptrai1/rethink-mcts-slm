from collections import deque
import sys

sys.setrecursionlimit(10**6)
input = sys.stdin.read
data = input().split()

Y = int(data[0])
X = int(data[1])
x_init = int(data[2])

map_data = [list(data[i + 3]) for i in range(Y)]

directions = [(0, 1), (0, -1), (-1, 0)]  # East, West, North
currents = {'>': (0, 1), '<': (0, -1)}

def bfs():
    dp = [[[-1] * 2 for _ in range(X)] for _ in range(Y)]
    dp[Y-1][x_init][0] = 0
    dp[Y-1][x_init][1] = 0
    
    queue = deque([(Y-1, x_init, 0), (Y-1, x_init, 1)])
    
    while queue:
        y, x, d = queue.popleft()
        
        if map_data[y][x] == '@':
            return dp[y][x][d]
        
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            
            if 0 <= ny < Y and 0 <= nx < X and map_data[ny][nx] != '#':
                if map_data[ny][nx] in currents:
                    nd = 1 - d
                else:
                    nd = d
                
                if dp[ny][nx][nd] == -1 or dp[y][x][d] + 1 < dp[ny][nx][nd]:
                    dp[ny][nx][nd] = dp[y][x][d] + 1
                    queue.append((ny, nx, nd))
                    
    return -1

result = bfs()
if result == -1:
    print("begin repairs")
else:
    print(result % 1000003)