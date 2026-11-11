import sys
from collections import defaultdict

def compute_depths(parents):
    depths = [0] * len(parents)
    for i in range(1, len(parents)):
        depths[i] = depths[parents[i]] + 1
    return depths

def dfs(node, depth, parents, order, visited, children):
    visited[node] = True
    order.append(node)
    for child in sorted(children[node]):
        if not visited[child]:
            dfs(child, depth + 1, parents, order, visited, children)

def process_query(u, k, order, depths):
    start_index = order.index(u)
    if start_index + k > len(order):
        return -1
    return order[start_index + k - 1]

def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    q = int(data[index + 1])
    index += 2
    
    parents = [0] * (n + 1)
    for i in range(1, n):
        parents[i + 1] = int(data[index + i - 1])
    
    children = defaultdict(list)
    for i in range(2, n + 1):
        children[parents[i]].append(i)
    
    depths = compute_depths(parents)
    
    order = []
    visited = [False] * (n + 1)
    dfs(1, 0, parents, order, visited, children)
    
    results = []
    for _ in range(q):
        u = int(data[index])
        k = int(data[index + 1])
        index += 2
        results.append(process_query(u, k, order, depths))
    
    print(" ".join(map(str, results)))

if __name__ == "__main__":
    solve()