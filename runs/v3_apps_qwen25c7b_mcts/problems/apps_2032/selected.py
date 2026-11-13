import sys
from collections import defaultdict, deque

def max_defended_score(n, m, k, castles, portals):
    # Initialize graph and DP table
    graph = defaultdict(list)
    dp = [[[-float('inf')] * 2 for _ in range(k + 1)] for _ in range(n)]
    
    # Build the graph
    for u, v in portals:
        graph[u].append(v)
    
    # Base case initialization
    for i in range(k + 1):
        dp[0][i][0] = 0
    
    # Fill the DP table
    for i in range(1, n):
        for j in range(k + 1):
            for l in range(2):
                if dp[i-1][j][l] == float('-inf'):
                    continue
                if j >= castles[i][0]:
                    dp[i][j-castles[i][0]][0] = max(dp[i][j-castles[i][0]][0], dp[i-1][j][l])
                if j >= castles[i][0] + 1:
                    dp[i][j-castles[i][0]-1][1] = max(dp[i][j-castles[i][0]-1][1], dp[i-1][j][l] + castles[i][2])
                for v in graph[i+1]:
                    if j >= castles[v-1][0]:
                        dp[v-1][j-castles[v-1][0]][0] = max(dp[v-1][j-castles[v-1][0]][0], dp[i][j][l])
    
    # Find the maximum score
    max_score = -float('inf')
    for j in range(k + 1):
        for l in range(2):
            max_score = max(max_score, dp[n-1][j][l])
    
    return max_score if max_score != -float('inf') else -1

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])

castles = []
index = 3
for _ in range(n):
    a = int(data[index])
    b = int(data[index + 1])
    c = int(data[index + 2])
    castles.append((a, b, c))
    index += 3

portals = []
for _ in range(m):
    u = int(data[index]) - 1
    v = int(data[index + 1]) - 1
    portals.append((u, v))
    index += 2

# Output the result
print(max_defended_score(n, m, k, castles, portals))