import sys
from collections import defaultdict, deque

def bfs(start, graph):
    queue = deque([start])
    dist = [-1] * len(graph)
    dist[start] = 0
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if dist[neighbor] == -1:
                dist[neighbor] = dist[node] + 1
                queue.append(neighbor)
    return dist

def find_longest_path(start, graph):
    dist = bfs(start, graph)
    farthest_node = dist.index(max(dist))
    return bfs(farthest_node, graph)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    edges = [(int(data[2*i+1])-1, int(data[2*i+2])-1) for i in range(n-1)]
    
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # Find the first longest path
    dist1 = find_longest_path(0, graph)
    farthest_node1 = dist1.index(max(dist1))
    
    # Find the second longest path starting from the farthest node of the first path
    dist2 = find_longest_path(farthest_node1, graph)
    farthest_node2 = dist2.index(max(dist2))
    
    # Find the third longest path starting from the farthest node of the second path
    dist3 = find_longest_path(farthest_node2, graph)
    farthest_node3 = dist3.index(max(dist3))
    
    # The result is the sum of the lengths of the three longest paths minus 2 (since the middle node is counted twice)
    res = max(dist1[farthest_node2] + dist2[farthest_node3], dist1[farthest_node3] + dist3[farthest_node2], dist2[farthest_node1] + dist1[farthest_node3])
    
    # Output the result
    print(res)
    print(farthest_node1 + 1, farthest_node2 + 1, farthest_node3 + 1)

if __name__ == "__main__":
    main()