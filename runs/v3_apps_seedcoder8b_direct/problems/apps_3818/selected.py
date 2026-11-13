import sys
from collections import defaultdict, deque

MOD = 10**9 + 7

def solve():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    edges = []
    
    index = 1
    for _ in range(N - 1):
        a = int(data[index])
        b = int(data[index + 1])
        edges.append((a, b))
        index += 2
    
    # Build the adjacency list for the tree
    tree = defaultdict(list)
    for a, b in edges:
        tree[a].append(b)
        tree[b].append(a)
    
    # Function to calculate the size of each subtree
    def dfs_size(node, parent):
        size[node] = 1
        for neighbor in tree[node]:
            if neighbor == parent:
                continue
            dfs_size(neighbor, node)
            size[node] += size[neighbor]
    
    # Function to calculate distances from a given node
    def bfs_distances(start):
        distances = [-1] * (N + 1)
        queue = deque([start])
        distances[start] = 0
        while queue:
            node = queue.popleft()
            for neighbor in tree[node]:
                if distances[neighbor] == -1:
                    distances[neighbor] = distances[node] + 1
                    queue.append(neighbor)
        return distances
    
    # Calculate the size of each subtree
    size = [0] * (N + 1)
    dfs_size(1, -1)
    
    # Find the centroid of the tree
    def find_centroid(node, parent):
        for neighbor in tree[node]:
            if neighbor == parent:
                continue
            if size[neighbor] > N // 2:
                return find_centroid(neighbor, node)
        return node
    
    centroid = find_centroid(1, -1)
    
    # Calculate distances from the centroid
    distances_from_centroid = bfs_distances(centroid)
    
    # Calculate the sum of distances for all vertices
    total_distance = sum(distances_from_centroid[1:])
    
    # Calculate the sum of the nicenesses
    result = (total_distance * total_distance) % MOD
    
    print(result)