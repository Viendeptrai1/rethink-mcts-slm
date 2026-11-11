import sys
from collections import defaultdict, deque

MOD = 10**9 + 7

def dfs(node, parent, graph, depth, max_depth):
    max_depth[node] = depth
    for neighbor in graph[node]:
        if neighbor != parent:
            dfs(neighbor, node, graph, depth + 1, max_depth)

def bfs(start, graph, n):
    queue = deque([start])
    distance = [-1] * n
    distance[start] = 0
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if distance[neighbor] == -1:
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
    return distance

def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    edges = [(int(data[2*i+1]) - 1, int(data[2*i+2]) - 1) for i in range(n-1)]
    
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    
    max_depth = [0] * n
    dfs(0, -1, graph, 0, max_depth)
    
    total_sum = 0
    
    for i in range(n):
        distances = bfs(i, graph, n)
        max_white = 0
        max_black = 0
        for j in range(n):
            if max_depth[j] >= max_depth[i]:
                max_white = max(max_white, distances[j])
            else:
                max_black = max(max_black, distances[j])
        total_sum += max(max_white, max_black)
        total_sum %= MOD
    
    print(total_sum)

if __name__ == "__main__":
    solve()