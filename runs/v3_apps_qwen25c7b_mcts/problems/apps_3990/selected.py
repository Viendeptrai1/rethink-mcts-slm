import heapq
from collections import defaultdict

def min_time_to_reach_n(n, m, railways):
    # Build the graph for railways
    rail_graph = defaultdict(list)
    for u, v in railways:
        rail_graph[u].append((v, 1))
        rail_graph[v].append((u, 1))

    # Function to find the shortest path using Dijkstra's algorithm
    def dijkstra(graph, start):
        distances = [float('inf')] * (n + 1)
        distances[start] = 0
        pq = [(0, start)]
        while pq:
            current_dist, u = heapq.heappop(pq)
            if current_dist > distances[u]:
                continue
            for v, weight in graph[u]:
                distance = current_dist + weight
                if distance < distances[v]:
                    distances[v] = distance
                    heapq.heappush(pq, (distance, v))
        return distances

    # Find the shortest path for the train
    train_times = dijkstra(rail_graph, 1)

    # Check if the bus can reach town n
    if train_times[n] == float('inf'):
        return -1

    # Build the graph for roads
    road_graph = defaultdict(list)
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if (i, j) not in railways and (j, i) not in railways:
                road_graph[i].append((j, 1))
                road_graph[j].append((i, 1))

    # Find the shortest path for the bus
    bus_times = dijkstra(road_graph, 1)

    # Determine the minimum time for both vehicles to reach town n
    max_time = max(train_times[n], bus_times[n])
    return max_time

# Example usage
if __name__ == "__main__":
    import sys
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
    
    result = min_time_to_reach_n(n, m, railways)
    print(result)