import sys
from heapq import heappop, heappush
from collections import defaultdict

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    index += 2
    
    a = list(map(int, data[index:index + n]))
    index += n
    
    segments = []
    for _ in range(m):
        l = int(data[index]) - 1
        r = int(data[index + 1]) - 1
        segments.append((l, r))
        index += 2
    
    # Create a graph where each node represents an array position
    graph = defaultdict(list)
    for i in range(n):
        graph[i].append((i, 0))  # Stay at the same position with no change
    
    for j, (l, r) in enumerate(segments):
        for i in range(l, r + 1):
            graph[i].append((i, -1))  # Move to the same position with a decrement
    
    # Dijkstra's algorithm to find the maximum difference
    max_diff = float('-inf')
    best_path = []
    
    for start in range(n):
        dist = [float('inf')] * n
        dist[start] = a[start]
        pq = [(a[start], start)]
        
        while pq:
            current_dist, u = heappop(pq)
            
            if current_dist > dist[u]:
                continue
            
            for v, weight in graph[u]:
                new_dist = current_dist + weight
                
                if new_dist > dist[v]:
                    dist[v] = new_dist
                    heappush(pq, (new_dist, v))
        
        current_max = max(dist)
        current_min = min(dist)
        current_diff = current_max - current_min
        
        if current_diff > max_diff:
            max_diff = current_diff
            best_start = start
            best_dist = dist[:]
    
    # Trace back the path to get the segments used
    used_segments = set()
    for i in range(n):
        if best_dist[i] == a[i]:
            continue
        for j, (l, r) in enumerate(segments):
            if l <= i <= r and best_dist[i] == best_dist[i - 1] - 1:
                used_segments.add(j)
                break
    
    print(max_diff)
    print(len(used_segments))
    print(*[j + 1 for j in sorted(used_segments)])

if __name__ == "__main__":
    main()