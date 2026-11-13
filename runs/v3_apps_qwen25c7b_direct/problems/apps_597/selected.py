import sys
from collections import defaultdict, deque

def bfs(graph, start):
    queue = deque([start])
    visited = set([start])
    distance = {start: 0}
    
    while queue:
        current = queue.popleft()
        
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                distance[neighbor] = distance[current] + 1
                queue.append(neighbor)
                
    return distance

def find_optimal_teleportation(n, m, edges, attacked_cities):
    graph = defaultdict(list)
    
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    min_time = float('inf')
    best_city = None
    
    for city in range(1, n + 1):
        distances = bfs(graph, city)
        total_time = sum(distances[city] for city in attacked_cities)
        
        if total_time < min_time or (total_time == min_time and city < best_city):
            min_time = total_time
            best_city = city
            
    return best_city, min_time

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    index += 2
    
    edges = []
    for _ in range(n - 1):
        u = int(data[index])
        v = int(data[index + 1])
        edges.append((u, v))
        index += 2
        
    attacked_cities = list(map(int, data[index:index + m]))
    
    result = find_optimal_teleportation(n, m, edges, attacked_cities)
    print(result[0])
    print(result[1])