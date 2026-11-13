import heapq
import sys

def shortest_paths_count(V, E, edges, s, t):
    # Initialize distances and the number of ways to reach each node
    dist = [float('inf')] * V
    ways = [0] * V
    dist[s] = 0
    ways[s] = 1

    # Min-heap to get the node with the smallest distance
    heap = [(0, s)]

    # Adjacency list representation of the graph
    graph = {i: [] for i in range(V)}
    for u, v, w in edges:
        graph[u].append((v, w))

    while heap:
        current_dist, u = heapq.heappop(heap)
        
        if u == t:
            break

        # Skip if a shorter path to u has been processed
        if current_dist > dist[u]:
            continue

        for v, weight in graph[u]:
            new_dist = current_dist + weight

            # If a new shortest path to v is found
            if new_dist < dist[v]:
                dist[v] = new_dist
                ways[v] = ways[u]
                heapq.heappush(heap, (new_dist, v))
            # If another shortest path to v is found with the same length
            elif new_dist == dist[v]:
                ways[v] += ways[u]

    return ways[t]

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()

    V = int(data[0])
    E = int(data[1])
    edges = []
    index = 2
    for _ in range(E):
        u = int(data[index])
        v = int(data[index + 1])
        w = int(data[index + 2])
        edges.append((u, v, w))
        index += 3

    s = int(data[index])
    t = int(data[index + 1])

    result = shortest_paths_count(V, E, edges, s, t)
    print(result)