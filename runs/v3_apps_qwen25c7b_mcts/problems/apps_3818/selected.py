import sys
from collections import defaultdict

MOD = 10**9 + 7

def dfs(node, parent):
    max_dist_white = [0]
    max_dist_black = [0]
    
    for neighbor in graph[node]:
        if neighbor != parent:
            dists = dfs(neighbor, node)
            max_dist_white.append(max(max_dist_white[-1], dists[0] + 1))
            max_dist_black.append(max(max_dist_black[-1], dists[1] + 1))
    
    total_niceness = 0
    for i in range(len(max_dist_white)):
        for j in range(i + 1, len(max_dist_black)):
            total_niceness += max(max_dist_white[i], max_dist_black[j])
    
    return max_dist_white[-1], max_dist_black[-1]

def count_ways():
    total_niceness = 0
    
    for root in range(1, n + 1):
        niceness = dfs(root, -1)[0]
        total_niceness += niceness
    
    return total_niceness % MOD

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
edges = [(int(data[2 * i + 1]), int(data[2 * i + 2])) for i in range(n - 1)]

# Build the graph
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)

# Calculate and print the result
print(count_ways())