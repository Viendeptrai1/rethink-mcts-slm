from sys import stdin, stdout
from collections import defaultdict, deque

def dfs(node, parent):
    stack = [(node, 0)]
    while stack:
        node, depth = stack.pop()
        if depth == len(order[node]):
            order[node].append(node)
        else:
            order[node][depth] = node
        for neighbor in graph[node]:
            if neighbor != parent:
                stack.append((neighbor, depth + 1))

def get_kth_subordinate(u, k):
    if k > len(order[u]):
        return -1
    return order[u][k - 1]

# Read input
input = stdin.read
data = input().split()

n = int(data[0])
q = int(data[1])

parents = list(map(int, data[2:n+1]))
graph = defaultdict(list)
order = defaultdict(list)

for i in range(2, n + 1):
    graph[parents[i-1]].append(i)

dfs(1, None)

queries = []
for i in range(q):
    u = int(data[n + 2 + 2 * i]) - 1
    k = int(data[n + 3 + 2 * i])
    queries.append((u, k))

# Process queries
results = []
for u, k in queries:
    results.append(get_kth_subordinate(u, k))

# Output results
stdout.write(' '.join(map(str, results)))