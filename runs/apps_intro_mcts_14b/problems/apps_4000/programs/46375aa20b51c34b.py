import sys
from collections import deque

def bfs(start, n, adj):
    dist = [-1] * n
    queue = deque([start])
    dist[start] = 0
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist

def find_diameter(n, adj):
    # First BFS to find one end of the diameter
    dist_from_0 = bfs(0, n, adj)
    farthest_node = dist_from_0.index(max(dist_from_0))
    
    # Second BFS to find the other end of the diameter
    dist_from_farthest = bfs(farthest_node, n, adj)
    second_farthest_node = dist_from_farthest.index(max(dist_from_farthest))
    
    return farthest_node, second_farthest_node, max(dist_from_farthest)

def find_third_vertex(diameter_end, n, adj):
    dist_from_diameter_end = bfs(diameter_end, n, adj)
    third_vertex = dist_from_diameter_end.index(max(dist_from_diameter_end))
    return third_vertex

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    adj = [[] for _ in range(n)]
    index = 1
    for _ in range(n - 1):
        u = int(data[index]) - 1
        v = int(data[index + 1]) - 1
        adj[u].append(v)
        adj[v].append(u)
        index += 2
    
    # Find the diameter of the tree
    first_diameter_end, second_diameter_end, diameter_length = find_diameter(n, adj)
    
    # Find the third vertex that maximizes the number of unique edges
    third_vertex = find_third_vertex(first_diameter_end, n, adj)
    
    # Calculate the number of unique edges covered by the paths
    res = diameter_length + max(bfs(second_diameter_end, n, adj)[third_vertex], bfs(third_vertex, n, adj)[second_diameter_end])
    
    # Output the result
    print(res + 1)
    print(f"{first_diameter_end + 1} {second_diameter_end + 1} {third_vertex + 1}")

if __name__ == "__main__":
    main()