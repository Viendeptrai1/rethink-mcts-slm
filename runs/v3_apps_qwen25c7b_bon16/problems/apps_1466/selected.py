import sys
from heapq import heappop, heappush
from collections import defaultdict, deque

def dijkstra(n, edges, start):
    dist = [float('inf')] * (n + 1)
    dist[start] = 0
    pq = [(0, start)]
    
    while pq:
        current_dist, u = heappop(pq)
        
        if current_dist > dist[u]:
            continue
        
        for v, weight in edges[u]:
            distance = current_dist + weight
            
            if distance < dist[v]:
                dist[v] = distance
                heappush(pq, (distance, v))
                
    return dist

def main():
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    k = int(data[index + 2])
    index += 3
    
    edges = defaultdict(list)
    for _ in range(m):
        x = int(data[index]) - 1
        y = int(data[index + 1]) - 1
        w = int(data[index + 2])
        edges[x].append((y, w))
        edges[y].append((x, w))
        index += 3
    
    d = dijkstra(n, edges, 0)
    
    good_edges = []
    for i in range(1, n + 1):
        if d[i] == float('inf'):
            continue
        for j in range(len(edges[i])):
            if d[i] == d[edges[i][j][0]] + edges[i][j][1]:
                good_edges.append(j + 1)
                break
                
    e = min(k, len(good_edges))
    print(e)
    print(" ".join(map(str, sorted(good_edges[:e]))))

if __name__ == "__main__":
    main()