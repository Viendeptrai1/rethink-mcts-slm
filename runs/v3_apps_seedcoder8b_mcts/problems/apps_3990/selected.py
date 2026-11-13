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
    
    # BFS to find shortest path from town 1 to town n for both train and bus
    def bfs(graph, start, end):
        queue = deque([(start, 0)])
        visited = {start: 0}
        while queue:
            current, time = queue.popleft()
            if current == end:
                return time
            for neighbor in graph[current]:
                if neighbor not in visited:
                    visited[neighbor] = time + 1
                    queue.append((neighbor, time + 1))
        return float('inf')
    
    train_time = bfs(railway_graph, 1, n)
    bus_time = bfs(road_graph, 1, n)
    
    # If either train or bus cannot reach town n, return -1
    if train_time == float('inf') or bus_time == float('inf'):
        return -1
    
    # Return the maximum of the two arrival times
    return max(train_time, bus_time)

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