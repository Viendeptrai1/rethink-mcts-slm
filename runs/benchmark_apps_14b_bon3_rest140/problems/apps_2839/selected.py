import sys
import heapq

def dijkstra(graph, start):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_vertex]:
            continue
        
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances

def count_shortest_paths(graph, start, end):
    distances = dijkstra(graph, start)
    if distances[end] == float('infinity'):
        return 0
    
    paths_count = [0] * len(graph)
    paths_count[start] = 1
    
    queue = [start]
    while queue:
        current = queue.pop(0)
        for neighbor, weight in graph[current].items():
            if distances[current] + weight == distances[neighbor]:
                paths_count[neighbor] += paths_count[current]
                if neighbor not in queue:
                    queue.append(neighbor)
    
    return paths_count[end]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    V = int(data[index])
    E = int(data[index + 1])
    index += 2
    
    graph = {i: {} for i in range(V)}
    
    for _ in range(E):
        u = int(data[index])
        v = int(data[index + 1])
        w = int(data[index + 2])
        graph[u][v] = w
        index += 3
    
    s = int(data[index])
    t = int(data[index + 1])
    
    result = count_shortest_paths(graph, s, t)
    print(result)

if __name__ == "__main__":
    main()