from collections import defaultdict

def count_failures(n, nodes):
    graph = defaultdict(list)
    root = None
    
    for i, (v, l, r) in enumerate(nodes):
        if l != -1:
            graph[i].append(l)
        if r != -1:
            graph[i].append(r)
        if l == -1 and r == -1:
            root = i
    
    def dfs(node, target):
        if node == -1:
            return False
        if nodes[node][0] == target:
            return True
        if nodes[node][0] > target:
            return dfs(graph[node][0], target)
        else:
            return dfs(graph[node][1], target)
    
    failures = 0
    for i in range(n):
        if not dfs(i, nodes[i][0]):
            failures += 1
    
    return failures

# Input reading
n = int(input())
nodes = [tuple(map(int, input().split())) for _ in range(n)]

# Output the result
print(count_failures(n, nodes))