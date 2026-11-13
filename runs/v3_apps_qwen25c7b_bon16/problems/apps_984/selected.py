import sys
from collections import defaultdict

def count_failures(n, nodes):
    graph = defaultdict(list)
    
    # Build adjacency list representation of the tree
    for i in range(n):
        v, l, r = nodes[i]
        if l != -1:
            graph[i].append(l)
        if r != -1:
            graph[i].append(r)
    
    failure_count = 0
    
    def dfs(node, target):
        nonlocal failure_count
        if node == -1:
            failure_count += 1
            return False
        if nodes[node][0] == target:
            return True
        elif nodes[node][0] > target:
            return dfs(nodes[node][1], target)
        else:
            return dfs(nodes[node][2], target)
    
    # Run DFS for each unique value in the tree
    seen_values = set()
    for i in range(n):
        v, _, _ = nodes[i]
        if v not in seen_values:
            seen_values.add(v)
            dfs(i, v)
    
    return failure_count

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
nodes = [(int(data[3*i+1]), int(data[3*i+2]), int(data[3*i+3])) for i in range(n)]

# Calculate and print the result
result = count_failures(n, nodes)
print(result)