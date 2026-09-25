import sys
from collections import defaultdict, deque

def find_centroid(n, adj):
    def dfs(node, parent):
        size[node] = 1
        max_subtree = 0
        for neighbor in adj[node]:
            if neighbor != parent:
                dfs(neighbor, node)
                size[node] += size[neighbor]
                max_subtree = max(max_subtree, size[neighbor])
        max_subtree = max(max_subtree, n - size[node])
        if max_subtree < min_size:
            min_size = max_subtree
            centroid = node

    size = [0] * n
    min_size = float('inf')
    centroid = -1
    dfs(0, -1)
    return centroid

def bfs_distance(start, n, adj):
    queue = deque([start])
    distance = [-1] * n
    distance[start] = 0
    while queue:
        node = queue.popleft()
        for neighbor in adj[node]:
            if distance[neighbor] == -1:
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
    return distance

def find_farthest_node(start, n, adj):
    distance = bfs_distance(start, n, adj)
    farthest_node = start
    max_distance = 0
    for i in range(n):
        if distance[i] > max_distance:
            max_distance = distance[i]
            farthest_node = i
    return farthest_node

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    adj = defaultdict(list)
    index = 1
    for _ in range(n - 1):
        a = int(data[index]) - 1
        b = int(data[index + 1]) - 1
        adj[a].append(b)
        adj[b].append(a)
        index += 2
    
    centroid = find_centroid(n, adj)
    farthest_from_centroid = find_farthest_node(centroid, n, adj)
    farthest_from_farthest = find_farthest_node(farthest_from_centroid, n, adj)
    
    res = bfs_distance(centroid, n, adj)[farthest_from_farthest] + 1
    print(res)
    print(farthest_from_centroid + 1, centroid + 1, farthest_from_farthest + 1)

if __name__ == "__main__":
    main()