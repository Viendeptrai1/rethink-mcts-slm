import sys
from collections import defaultdict, deque

def max_score(n, m, k, castles, portals):
    # Unpack the castles data
    a = [castle[0] for castle in castles]
    b = [castle[1] for castle in castles]
    c = [castle[2] for castle in castles]
    
    # Create adjacency list for portals
    adj = defaultdict(list)
    for u, v in portals:
        adj[u].append(v)
    
    # Initialize DP table
    dp = [[-float('inf')] * (k + 1) for _ in range(n + 1)]
    dp[0][k] = 0
    
    # Iterate over each castle
    for i in range(1, n + 1):
        for j in range(k + 1):
            if dp[i - 1][j] == -float('inf'):
                continue
            
            # Option 1: Capture the i-th castle
            if j >= a[i - 1]:
                new_army = j - a[i - 1] + b[i - 1]
                dp[i][new_army] = max(dp[i][new_army], dp[i - 1][j])
            
            # Option 2: Defend the i-th castle
            if j > 0:
                dp[i][j - 1] = max(dp[i][j - 1], dp[i - 1][j] + c[i - 1])
            
            # Option 3: Use portals to defend other castles
            for v in adj[i]:
                if j > 0:
                    dp[v][j - 1] = max(dp[v][j - 1], dp[i - 1][j] + c[v - 1])
    
    # Calculate the maximum score
    max_score = -1
    for j in range(k + 1):
        max_score = max(max_score, dp[n][j])
    
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
    a_i = int(data[index])
    b_i = int(data[index + 1])
    c_i = int(data[index + 2])
    castles.append((a_i, b_i, c_i))
    index += 3
portals = []
for _ in range(m):
    u_i = int(data[index])
    v_i = int(data[index + 1])
    portals.append((u_i, v_i))
    index += 2

# Output the result
print(max_score(n, m, k, castles, portals))