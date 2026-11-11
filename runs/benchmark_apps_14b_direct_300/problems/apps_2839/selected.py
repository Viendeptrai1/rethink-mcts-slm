import sys
import heapq

def count_shortest_paths(V, E, edges, s, t):
    # Initialize distance and path count arrays
    dist = [float('inf')] * V
    path_count = [0] * V
    
    # Priority queue for Dijkstra's algorithm
    pq = []
    
    # Start from source vertex
    dist[s] = 0
    path_count[s] = 1
    heapq.heappush(pq, (0, s))
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        
        # If we reach the destination, return the path count
        if u == t:
            return path_count[t]
        
        # If the current distance is greater than the recorded distance, skip
        if current_dist > dist[u]:
            continue
        
        # Explore neighbors
        for v, weight in edges[u]:
            if current_dist + weight < dist[v]:
                dist[v] = current_dist + weight
                path_count[v] = path_count[u]
                heapq.heappush(pq, (dist[v], v))
            elif current_dist + weight == dist[v]:
                path_count[v] += path_count[u]
    
    # If we cannot reach the destination, return 0
    return 0

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    V = int(data[index])
    E = int(data[index + 1])
    index += 2
    
    edges = [[] for _ in range(V)]
    
    for _ in range(E):
        u = int(data[index])
        v = int(data[index + 1])
        weight = int(data[index + 2])
        edges[u].append((v, weight))
        index += 3
    
    s = int(data[index])
    t = int(data[index + 1])
    
    result = count_shortest_paths(V, E, edges, s, t)
    print(result)

if __name__ == "__main__":
    main()