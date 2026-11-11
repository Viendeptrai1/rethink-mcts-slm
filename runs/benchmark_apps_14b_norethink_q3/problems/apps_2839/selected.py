import sys
import heapq

def dijkstra_count_paths(graph, V, s, t):
    # Distance array to store the shortest distance from s to each vertex
    dist = [float('inf')] * V
    # Path count array to store the number of shortest paths from s to each vertex
    path_count = [0] * V
    # Priority queue to process vertices based on their distance from s
    pq = [(0, s)]
    
    dist[s] = 0
    path_count[s] = 1
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        
        if current_dist > dist[u]:
            continue
        
        for v, weight in graph[u]:
            if current_dist + weight < dist[v]:
                dist[v] = current_dist + weight
                path_count[v] = path_count[u]
                heapq.heappush(pq, (dist[v], v))
            elif current_dist + weight == dist[v]:
                path_count[v] += path_count[u]
    
    return path_count[t]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    V = int(data[index])
    E = int(data[index + 1])
    index += 2
    
    graph = [[] for _ in range(V)]
    
    for _ in range(E):
        u = int(data[index])
        v = int(data[index + 1])
        w = int(data[index + 2])
        graph[u].append((v, w))
        index += 3
    
    s = int(data[index])
    t = int(data[index + 1])
    
    result = dijkstra_count_paths(graph, V, s, t)
    print(result)

if __name__ == "__main__":
    main()