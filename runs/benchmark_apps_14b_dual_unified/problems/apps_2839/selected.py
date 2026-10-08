import sys
import heapq

def dijkstra_count_paths(graph, start, end):
    n = len(graph)
    distances = [float('inf')] * n
    distances[start] = 0
    paths = [0] * n
    paths[start] = 1
    pq = [(0, start)]
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        
        if u == end:
            return paths[u]
        
        if current_dist > distances[u]:
            continue
        
        for v, weight in graph[u]:
            distance = current_dist + weight
            
            if distance < distances[v]:
                distances[v] = distance
                paths[v] = paths[u]
                heapq.heappush(pq, (distance, v))
            elif distance == distances[v]:
                paths[v] += paths[u]
    
    return paths[end]

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
    
    result = dijkstra_count_paths(graph, s, t)
    print(result)

if __name__ == "__main__":
    main()