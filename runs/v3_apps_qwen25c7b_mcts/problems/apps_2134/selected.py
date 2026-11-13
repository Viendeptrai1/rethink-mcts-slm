import sys
from collections import defaultdict, deque

def bfs_max_matching(graph, n):
    visited = [False] * n
    match = [-1] * n
    parent = [-1] * n
    
    def bfs(u):
        queue = deque([u])
        visited[u] = True
        while queue:
            u = queue.popleft()
            for v in range(n):
                if not visited[v] and graph[u][v]:
                    visited[v] = True
                    parent[v] = u
                    if match[v] == -1 or bfs(match[v]):
                        match[v] = u
                        return True
        return False
    
    max_match = 0
    for u in range(n):
        if match[u] == -1:
            visited = [False] * n
            if bfs(u):
                max_match += 1
    return max_match

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:n+1]))
    b = list(map(int, data[n+1:2*n+1]))
    
    graph = [[False] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(i + 1, n):
            if (a[i] & a[j]) == 0:
                graph[i][j] = True
                graph[j][i] = True
    
    max_match = bfs_max_matching(graph, n)
    
    if max_match >= 2:
        result = sum(b[i] for i in range(n) if match[i] != -1)
        print(result)
    else:
        print(0)

if __name__ == "__main__":
    main()