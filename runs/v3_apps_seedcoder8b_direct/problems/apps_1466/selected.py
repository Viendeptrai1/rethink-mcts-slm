import sys
import heapq
from collections import defaultdict

def find_good_vertices(n, m, k, edges):
    # Create adjacency list
    graph = defaultdict(list)
    for i, (x, y, w) in enumerate(edges):
        graph[x].append((y, w, i + 1))
        graph[y].append((x, w, i + 1))
    
    # Dijkstra's algorithm to find shortest paths from vertex 1
    def dijkstra(start):
        dist = {i: float('inf') for i in range(1, n + 1)}
        dist[start] = 0
        pq = [(0, start)]
        while pq:
            d, node = heapq.heappop(pq)
            if d > dist[node]:
                continue
            for neighbor, weight, _ in graph[node]:
                if dist[node] + weight < dist[neighbor]:
                    dist[neighbor] = dist[node] + weight
                    heapq.heappush(pq, (dist[neighbor], neighbor))
        return dist
    
    # Find shortest paths from vertex 1
    shortest_paths = dijkstra(1)
    
    # Sort edges by weight in descending order
    sorted_edges = sorted(enumerate(edges, 1), key=lambda x: x[1][2], reverse=True)
    
    # Initialize set of edges to keep
    edges_to_keep = set()
    
    # Function to check if removing an edge increases the number of good vertices
    def is_good_after_removal(edge_index):
        x, y, w = edges[edge_index - 1]
        if shortest_paths[x] + w == shortest_paths[y] or shortest_paths[y] + w == shortest_paths[x]:
            return False
        return True
    
    # Greedily select edges to keep
    for edge_index, _ in sorted_edges:
        if len(edges_to_keep) < k and is_good_after_removal(edge_index):
            edges_to_keep.add(edge_index)
    
    # Output the result
    print(len(edges_to_keep))
    if edges_to_keep:
        print(*sorted(edges_to_keep))

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    k = int(data[2])
    
    edges = []
    index = 3
    for _ in range(m):
        x = int(data[index])
        y = int(data[index + 1])
        w = int(data[index + 2])
        edges.append((x, y, w))
        index += 3
    
    find_good_vertices(n, m, k, edges)

if __name__ == "__main__":
    main()