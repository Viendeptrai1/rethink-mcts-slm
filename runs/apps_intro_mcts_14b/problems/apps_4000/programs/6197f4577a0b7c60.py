import sys
from collections import defaultdict, deque

def bfs(start, adj):
    dist = [-1] * (n + 1)
    queue = deque([start])
    dist[start] = 0
    farthest = start
    max_dist = 0
    
    while queue:
        node = queue.popleft()
        for neighbor in adj[node]:
            if dist[neighbor] == -1:
                dist[neighbor] = dist[node] + 1
                queue.append(neighbor)
                if dist[neighbor] > max_dist:
                    max_dist = dist[neighbor]
                    farthest = neighbor
    
    return farthest, max_dist, dist

def find_longest_paths():
    # Find the farthest node from an arbitrary starting node (node 1)
    farthest1, _, _ = bfs(1, adj)
    
    # Find the farthest node from the farthest node found in the previous step
    farthest2, max_dist2, dist2 = bfs(farthest1, adj)
    
    # Find the farthest node from the farthest node found in the previous step
    farthest3, max_dist3, dist3 = bfs(farthest2, adj)
    
    # Find the farthest node from the farthest node found in the previous step
    farthest4, max_dist4, dist4 = bfs(farthest3, adj)
    
    # The three longest paths are from farthest1 to farthest2, farthest2 to farthest3, and farthest3 to farthest4
    return [farthest1, farthest2, farthest3, farthest4], [max_dist2, max_dist3, max_dist4]

def main():
    global n, adj
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    index += 1
    
    adj = defaultdict(list)
    for _ in range(n - 1):
        a = int(data[index])
        index += 1
        b = int(data[index])
        index += 1
        adj[a].append(b)
        adj[b].append(a)
    
    farthest_nodes, max_dists = find_longest_paths()
    
    # Select the three nodes that give the maximum coverage of edges
    res = max_dists[0] + max_dists[1] + max_dists[2]
    a, b, c = farthest_nodes[0], farthest_nodes[1], farthest_nodes[2]
    
    print(res)
    print(a, b, c)

if __name__ == "__main__":
    main()