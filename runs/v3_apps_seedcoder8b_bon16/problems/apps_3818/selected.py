import sys
from collections import defaultdict

MOD = 10**9 + 7

def solve():
    N = int(sys.stdin.readline())
    graph = defaultdict(list)
    
    for _ in range(N-1):
        a, b = map(int, sys.stdin.readline().split())
        graph[a].append(b)
        graph[b].append(a)
    
    def dfs(node, parent):
        size = 1
        depths = [0]
        for child in graph[node]:
            if child != parent:
                child_size, child_depths = dfs(child, node)
                size += child_size
                depths.extend([d+1 for d in child_depths])
        return size, depths
    
    _, depths = dfs(1, -1)
    total = sum(depths)
    n = len(depths)
    
    result = 0
    for d in depths:
        result += d * (n - d)
        result %= MOD
    
    result = (result * pow(n * (n-1) // 2, MOD-2, MOD)) % MOD
    result = (result * 2) % MOD
    
    print(result)

solve()