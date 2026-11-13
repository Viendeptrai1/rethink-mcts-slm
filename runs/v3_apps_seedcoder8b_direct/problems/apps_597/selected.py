import sys
from collections import deque, defaultdict

def bfs(start, graph, n):
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
    
    # Find the farthest city from any city using BFS
    # Start from an arbitrary city, say city 1
    distance_from_start = bfs(1, graph, n)
    farthest_city = 1
    for city in range(1, n + 1):
        if distance_from_start[city] > distance_from_start[farthest_city]:
            farthest_city = city
    
    # Find the farthest city from the farthest city found above
    distance_from_farthest = bfs(farthest_city, graph, n)
    teleport_city = farthest_city
    max_distance = 0
    for city in range(1, n + 1):
        if distance_from_farthest[city] > max_distance:
            max_distance = distance_from_farthest[city]
            teleport_city = city
    
    # Calculate the minimum time to reach all attacked cities
    min_time = 0
    for city in attacked_cities:
        min_time += min(distance_from_farthest[city], distance_from_start[city])
    
    return teleport_city, min_time

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
    
    teleport_city, min_time = find_best_teleport_city(n, m, roads, attacked_cities)
    print(teleport_city)
    print(min_time)

if __name__ == "__main__":
    main()