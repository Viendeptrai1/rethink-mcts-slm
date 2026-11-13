from collections import defaultdict
import heapq

def min_delivery_time(n, m, deliveries):
    # Build the graph
    graph = defaultdict(list)
    for src, dest in deliveries:
        graph[src].append(dest)
    
    # Function to calculate the minimum time to deliver candies starting from a given station
    def bfs(start):
        visited = [False] * (n + 1)
        distance = [-1] * (n + 1)
        pq = []
        
        # Add all deliveries starting from the current station
        for src, dest in deliveries:
            if src == start:
                heapq.heappush(pq, (0, dest))
        
        while pq:
            dist, node = heapq.heappop(pq)
            if visited[node]:
                continue
            visited[node] = True
            distance[node] = dist
            
            # Visit all neighbors
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    heapq.heappush(pq, (dist + 1, neighbor))
        
        return sum(max(0, d - (start - 1)) for d in distance if d != -1)
    
    # Calculate the minimum delivery time for each station
    result = [bfs(i + 1) for i in range(n)]
    
    return ' '.join(map(str, result))

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
deliveries = [(int(data[i*2 + 2]), int(data[i*2 + 3])) for i in range(m)]

# Output the result
print(min_delivery_time(n, m, deliveries))