import sys
from collections import defaultdict, deque

MOD = 10**9 + 7

def dfs(graph, root):
    stack = [(root, -1)]
    depth = {root: 0}
    parent = {root: None}
    
    while stack:
        node, par = stack.pop()
        for neighbor in graph[node]:
            if neighbor != par:
                parent[neighbor] = node
                depth[neighbor] = depth[node] + 1
                stack.append((neighbor, node))
    
    return depth, parent

def bfs(graph, start):
    queue = deque([start])
    distance = {start: 0}
    
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in distance:
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
    
    return distance

def max_distance(graph, root):
    depth, parent = dfs(graph, root)
    farthest_node = max(depth, key=depth.get)
    distance = bfs(graph, farthest_node)
    return max(distance.values())

def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    edges = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(N-1)]
    
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    
    total_sum = 0
    
    for i in range(1, 1 << N):
        white_nodes = [j+1 for j in range(N) if i & (1 << j)]
        
        if not white_nodes:
            total_sum += 0
            continue
        
        max_white_dist = max_distance(graph, white_nodes[0])
        
        black_nodes = [j+1 for j in range(1, N+1) if j not in white_nodes]
        
        if not black_nodes:
            total_sum += 0
            continue
        
        max_black_dist = max_distance(graph, black_nodes[0])
        
        total_sum += max(max_white_dist, max_black_dist)
        total_sum %= MOD
    
    print(total_sum)

if __name__ == "__main__":
    solve()