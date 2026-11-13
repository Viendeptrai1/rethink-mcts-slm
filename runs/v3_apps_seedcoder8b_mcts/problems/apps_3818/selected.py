import sys
from collections import deque, defaultdict

MOD = 10**9 + 7

def solve():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    edges = [(int(data[i*2+1])-1, int(data[i*2+2])-1) for i in range(N-1)]
    
    # Build the adjacency list for the tree
    adj = defaultdict(list)
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Function to calculate distances from a given start node using BFS
    def bfs(start):
        dist = [-1] * N
        dist[start] = 0
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for neighbor in adj[node]:
                if dist[neighbor] == -1:
                    dist[neighbor] = dist[node] + 1
                    queue.append(neighbor)
        return dist
    
    # Calculate distances from an arbitrary node (e.g., node 0)
    distances_from_0 = bfs(0)
    
    # Find the farthest node from node 0
    farthest_node = distances_from_0.index(max(distances_from_0))
    
    # Calculate distances from the farthest node found
    distances_from_farthest = bfs(farthest_node)
    
    # Find the diameter of the tree
    diameter = max(distances_from_farthest)
    
    # Calculate the number of ways to paint the tree
    num_ways = pow(2, N, MOD)
    
    # Calculate the sum of the nicenesses
    # The niceness is the maximum distance between any two nodes
    # Since the tree is symmetric, the niceness is the diameter
    sum_niceness = (diameter * num_ways) % MOD
    
    print(sum_niceness)