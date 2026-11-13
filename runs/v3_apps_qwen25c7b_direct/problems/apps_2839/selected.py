import sys
from heapq import heappop, heappush

def dijkstra(graph, start):
    n = len(graph)
    dist = [float('inf')] * n
    dist[start] = 0
    pq = [(0, start)]
    
    while pq:
        current_dist, u = heappop(pq)
        
        if current_dist > dist[u]:
            continue
        
        for v, weight in graph[u]:
            distance = current_dist + weight
            
            if distance < dist[v]:
                dist[v] = distance
                heappush(pq, (distance, v))
                
    return dist

def count_paths(graph, start, end, target_dist):
    n = len(graph)
    dp = [[0] * n for _ in range(target_dist + 1)]
    dp[0][start] = 1
    
    for d in range(1, target_dist + 1):
        for u in range(n):
            for v, weight in graph[u]:
                if dp[d - weight][u] > 0:
                    dp[d][v] += dp[d - weight][u]
                    
    return dp[target_dist][end]

def main():
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    V = int(data[index])
    E = int(data[index + 1])
    index += 2
    
    graph = [[] for _ in range(V)]
    for _ in range(E):
        u = int(data[index])
        v = int(data[index + 1])
        w = int(data[index + 2])
        graph[u].append((v, w))
        index += 3
    
    s = int(data[index])
    t = int(data[index + 1])
    
    dist = dijkstra(graph, s)
    if dist[t] == float('inf'):
        print(0)
    else:
        print(count_paths(graph, s, t, dist[t]))

if __name__ == "__main__":
    main()