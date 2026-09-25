import sys
from collections import defaultdict

def main():
    import sys
    import heapq
    
    def read_ints():
        return list(map(int, sys.stdin.readline().split()))
    
    n, m = read_ints()
    a = read_ints()
    segments = [read_ints() for _ in range(m)]
    
    # Create a graph where each node is an index in the array
    graph = defaultdict(list)
    for i in range(n):
        graph[i].append((i, 0))  # Edge to itself with weight 0
    
    # Add edges for each segment
    for j, (l, r) in enumerate(segments, start=1):
        for i in range(l-1, r):
            graph[i].append((i+1, 1))
            graph[i+1].append((i, 1))
    
    # Dijkstra's algorithm to find the shortest path from each node to all other nodes
    def dijkstra(start):
        dist = [float('inf')] * n
        dist[start] = 0
        pq = [(0, start)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in graph[u]:
                if dist[v] > dist[u] + w:
                    dist[v] = dist[u] + w
                    heapq.heappush(pq, (dist[v], v))
        return dist
    
    # Find the maximum and minimum values in the array after applying the segments
    max_diff = 0
    best_segments = []
    for i in range(n):
        dist = dijkstra(i)
        min_val = min(a[j] - dist[j] for j in range(n))
        max_val = max(a[j] - dist[j] for j in range(n))
        diff = max_val - min_val
        if diff > max_diff:
            max_diff = diff
            best_segments = [j+1 for j in range(m) if dist[segments[j][0]-1] < dist[segments[j][1]-1]]
    
    print(max_diff)
    print(len(best_segments))
    print(*best_segments)

if __name__ == "__main__":
    main()