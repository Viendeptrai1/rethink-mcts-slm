import sys
from collections import defaultdict

sys.setrecursionlimit(200000)

def process_queries(n, q, parents, queries):
    # Build the tree
    tree = defaultdict(list)
    for i in range(2, n + 1):
        tree[parents[i-2]].append(i)
    
    # DFS function to traverse the tree and build the spreading order
    def dfs(node):
        order.append(node)
        for child in tree[node]:
            dfs(child)
    
    results = []
    for u, k in queries:
        order = []
        dfs(u)
        if k <= len(order):
            results.append(order[k-1])
        else:
            results.append(-1)
    
    return results

# Read input
n, q = map(int, input().split())
parents = list(map(int, input().split()))
queries = [list(map(int, input().split())) for _ in range(q)]

# Process queries and print results
results = process_queries(n, q, parents, queries)
for result in results:
    print(result)