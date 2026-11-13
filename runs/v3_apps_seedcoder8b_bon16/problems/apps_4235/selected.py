import sys
from collections import defaultdict

def solve():
    n, m = map(int, input().split())
    graph = defaultdict(list)
    edges = []
    
    for _ in range(m):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)
        edges.append((u, v))
    
    visited = [False] * (n + 1)
    parent = [0] * (n + 1)
    
    def dfs(v, p):
        visited[v] = True
        parent[v] = p
        for u in graph[v]:
            if not visited[u]:
                if dfs(u, v):
                    return True
            elif u != p and u != parent[p]:
                return True
        return False
    
    if dfs(1, 0):
        print("NO")
    else:
        print("YES")
        orientation = [0] * m
        for i, (u, v) in enumerate(edges):
            if parent[v] == u:
                orientation[i] = 1
        print(''.join(map(str, orientation)))

if __name__ == "__main__":
    solve()