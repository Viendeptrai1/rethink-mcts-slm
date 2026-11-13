from sys import setrecursionlimit
import sys
input = sys.stdin.read
data = input().split()

def dfs(node):
    stack = [(node, 0)]
    while stack:
        node, pos = stack.pop()
        if pos == len(order[node]):
            order[node].append(node)
        else:
            order[node].append(order[order[node][pos]][pos + 1])
        for child in reversed(graph[node]):
            stack.append((child, 0))

n = int(data[0])
q = int(data[1])

graph = [[] for _ in range(n + 1)]
for i in range(2, n + 1):
    graph[int(data[i])].append(i)

order = [[] for _ in range(n + 1)]

setrecursionlimit(10**6)
dfs(1)

results = []
index = n + 2
for i in range(q):
    u = int(data[index])
    k = int(data[index + 1])
    index += 2
    if k > len(order[u]):
        results.append(-1)
    else:
        results.append(order[u][k - 1])

print(*results)