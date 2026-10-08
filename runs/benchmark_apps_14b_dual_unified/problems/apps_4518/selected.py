import sys
from collections import defaultdict, deque

def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    results = []
    
    for _ in range(t):
        n = int(data[index])
        index += 1
        a = list(map(int, data[index:index + n]))
        index += n
        
        # Create a graph where nodes are gangs and edges are districts
        graph = defaultdict(list)
        for i in range(n):
            graph[a[i]].append(i)
        
        # Check if we can form a spanning tree without connecting districts of the same gang
        if len(graph) < n - 1:
            results.append("NO")
            continue
        
        # Try to build the spanning tree
        visited = [False] * n
        edges = []
        
        def bfs(start):
            queue = deque([start])
            visited[start] = True
            while queue:
                u = queue.popleft()
                for v in range(n):
                    if not visited[v] and a[u] != a[v]:
                        visited[v] = True
                        edges.append((u + 1, v + 1))
                        queue.append(v)
        
        # Start BFS from any district
        bfs(0)
        
        # Check if all districts are visited
        if all(visited):
            results.append("YES")
            results.extend(f"{x} {y}" for x, y in edges)
        else:
            results.append("NO")
    
    print("\n".join(results))

if __name__ == "__main__":
    solve()