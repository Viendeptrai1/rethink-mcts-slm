import sys
from collections import deque, defaultdict

def bfs_distance(start, n, graph):
    distance = [-1] * (n + 1)
    queue = deque([start])
    distance[start] = 0
    while queue:
        current = queue.popleft()
        for neighbor in graph[current]:
            if distance[neighbor] == -1:
                distance[neighbor] = distance[current] + 1
                queue.append(neighbor)
    return distance

def find_best_teleport_city(n, m, roads, attacked_cities):
    graph = defaultdict(list)
    for u, v in roads:
        graph[u].append(v)
        graph[v].append(u)
    
    min_time = float('inf')
    best_city = -1
    
    for city in range(1, n + 1):
        distances = bfs_distance(city, n, graph)
        max_distance = max(distances[attacked_city] for attacked_city in attacked_cities)
        if max_distance < min_time:
            min_time = max_distance
            best_city = city
    
    return best_city, min_time

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    
    roads = []
    index = 2
    for _ in range(n - 1):
        u = int(data[index])
        v = int(data[index + 1])
        roads.append((u, v))
        index += 2
    
    attacked_cities = []
    for _ in range(m):
        attacked_cities.append(int(data[index]))
        index += 1
    
    best_city, min_time = find_best_teleport_city(n, m, roads, attacked_cities)
    print(best_city)
    print(min_time)

if __name__ == "__main__":
    main()