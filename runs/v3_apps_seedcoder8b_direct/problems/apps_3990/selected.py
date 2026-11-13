from collections import deque, defaultdict
import sys

def minimum_arrival_time(n, m, railways):
    # Create adjacency lists for railways and roads
    railway_graph = defaultdict(list)
    road_graph = defaultdict(list)

    # Populate the railway graph
    for u, v in railways:
        railway_graph[u].append(v)
        railway_graph[v].append(u)

    # Populate the road graph
    for x in range(1, n + 1):
        for y in range(1, n + 1):
            if x != y and (x, y) not in railways and (y, x) not in railways:
                road_graph[x].append(y)
                road_graph[y].append(x)

    # BFS to find shortest path in terms of edges
    def bfs(graph, start):
        distances = [-1] * (n + 1)
        distances[start] = 0
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if distances[neighbor] == -1:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)
        return distances

    # Get shortest paths from town 1
    train_distances = bfs(railway_graph, 1)
    bus_distances = bfs(road_graph, 1)

    # If either train or bus cannot reach town n, return -1
    if train_distances[n] == -1 or bus_distances[n] == -1:
        return -1

    # Find the minimum time for the later vehicle to reach town n
    min_time = float('inf')
    for town in range(1, n + 1):
        if train_distances[town] != -1 and bus_distances[town] != -1:
            max_arrival_time = max(train_distances[town], bus_distances[town])
            min_time = min(min_time, max_arrival_time)

    return min_time

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    railways = []
    
    index = 2
    for _ in range(m):
        u = int(data[index])
        v = int(data[index + 1])
        railways.append((u, v))
        index += 2
    
    result = minimum_arrival_time(n, m, railways)
    print(result)

if __name__ == "__main__":
    main()