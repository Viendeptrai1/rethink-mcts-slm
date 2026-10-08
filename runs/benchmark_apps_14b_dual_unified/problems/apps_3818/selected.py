import sys
from collections import defaultdict, deque

MOD = 10**9 + 7

def bfs(graph, start):
    n = len(graph)
    dist = [-1] * n
    queue = deque([start])
    dist[start] = 0
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if dist[neighbor] == -1:
                dist[neighbor] = dist[node] + 1
                queue.append(neighbor)
    return dist

def max_distance(graph, n):
    max_dist = [0] * n
    for i in range(n):
        dist = bfs(graph, i)
        max_dist[i] = max(dist)
    return max_dist

def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    edges = [(int(data[2*i+1])-1, int(data[2*i+2])-1) for i in range(n-1)]
    
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    
    max_dist = max_distance(graph, n)
    
    total_sum = 0
    for i in range(1 << n):
        white_max = 0
        black_max = 0
        for j in range(n):
            if i & (1 << j):
                white_max = max(white_max, max_dist[j])
            else:
                black_max = max(black_max, max_dist[j])
        total_sum += max(white_max, black_max)
        total_sum %= MOD
    
    print(total_sum)

if __name__ == "__main__":
    solve()