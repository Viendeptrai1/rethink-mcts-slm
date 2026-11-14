import sys
import heapq

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        V = int(next(iterator))
        E = int(next(iterator))
    except StopIteration:
        return

    adj = [[] for _ in range(V)]
    for _ in range(E):
        u = int(next(iterator))
        v = int(next(iterator))
        w = int(next(iterator))
        adj[u].append((v, w))

    try:
        s = int(next(iterator))
        t = int(next(iterator))
    except StopIteration:
        return

    if s == t:
        print(1)
        return

    # Dijkstra to find shortest distances
    dist = [float('inf')] * V
    dist[s] = 0
    pq = [(0, s)]
    
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))

    if dist[t] == float('inf'):
        print(0)
        return

    # Count shortest paths using DP on topological order of shortest path DAG
    # We only consider edges (u, v) where dist[u] + w == dist[v]
    # Since edge weights are positive, the shortest path DAG is acyclic and can be processed by sorting nodes by distance
    
    # Filter nodes that are reachable and part of some shortest path to t
    # Actually, we can just process all nodes in increasing order of dist
    # But we need to ensure we process in an order where u comes before v if u->v is on a shortest path
    # Sorting by dist guarantees this because w > 0 implies dist[u] < dist[v]
    
    nodes_by_dist = sorted(range(V), key=lambda x: dist[x])
    
    count = [0] * V
    count[s] = 1
    
    for u in nodes_by_dist:
        if dist[u] == float('inf'):
            continue
        if count[u] == 0:
            continue
        for v, w in adj[u]:
            if dist[u] + w == dist[v]:
                count[v] += count[u]
                # Check for overflow? Problem says answer fits in 32-bit signed integer.
                # However, intermediate counts might exceed if not careful, but since final answer fits, and we only add positive counts,
                # and we stop once we pass t? No, we need to propagate through the whole DAG.
                # Given the constraint, we assume it won't overflow standard Python integers (arbitrary precision).
    
    print(count[t])

if __name__ == "__main__":
    solve()