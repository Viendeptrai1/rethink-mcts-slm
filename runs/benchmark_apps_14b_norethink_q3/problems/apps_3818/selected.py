import sys
from collections import defaultdict, deque

MOD = 10**9 + 7

def dfs(node, parent, graph, depth, max_depth):
    max_depth[node] = depth
    for neighbor in graph[node]:
        if neighbor != parent:
            dfs(neighbor, node, graph, depth + 1, max_depth)

def bfs(start, graph, n):
    queue = deque([(start, 0)])
    visited = [False] * (n + 1)
    visited[start] = True
    farthest_node = start
    farthest_distance = 0
    
    while queue:
        node, distance = queue.popleft()
        if distance > farthest_distance:
            farthest_node = node
            farthest_distance = distance
        for neighbor in graph[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append((neighbor, distance + 1))
    
    return farthest_node, farthest_distance

def diameter(graph, n):
    _, d1 = bfs(1, graph, n)
    farthest_node, _ = bfs(d1, graph, n)
    return bfs(farthest_node, graph, n)[1]

def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    edges = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(n-1)]
    
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    
    total_sum = 0
    
    for i in range(1, n + 1):
        max_depth = [0] * (n + 1)
        dfs(i, -1, graph, 0, max_depth)
        
        max_white_distance = max(max_depth)
        max_black_distance = diameter(graph, n) - max_white_distance
        
        total_sum += max(max_white_distance, max_black_distance)
        total_sum %= MOD
    
    print(total_sum)

if __name__ == "__main__":
    solve()