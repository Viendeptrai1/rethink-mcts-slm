import sys

# Increase recursion depth just in case, though we will use iterative BFS
sys.setrecursionlimit(300005)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        m = int(next(iterator))
        k = int(next(iterator))
    except StopIteration:
        return

    # Store edges: (u, v, w, index)
    # We need to output indices (1-based)
    edges = []
    for i in range(m):
        u = int(next(iterator))
        v = int(next(iterator))
        w = int(next(iterator))
        edges.append((u, v, w, i + 1))

    # If k is 0, we cannot keep any edges.
    if k == 0:
        print(0)
        print()
        return

    # Build adjacency list for Dijkstra
    # adj[u] = list of (v, w, edge_index)
    adj = [[] for _ in range(n + 1)]
    for idx, (u, v, w, _) in enumerate(edges):
        adj[u].append((v, w, idx + 1))
        adj[v].append((u, w, idx + 1))

    # Dijkstra's algorithm to find shortest distances from vertex 1
    import heapq
    dist = [-1] * (n + 1)
    dist[1] = 0
    pq = [(0, 1)]  # (distance, vertex)

    while pq:
        d, u = heapq.heappop(pq)
        
        if dist[u] != -1 and d > dist[u]:
            continue
        
        for v, w, _ in adj[u]:
            if dist[v] == -1 or dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))

    # Now we need to select at most k edges such that the number of vertices v 
    # with a path of length dist[v] from 1 is maximized.
    # A vertex v is "good" if we can reach it with distance dist[v].
    # This happens if we include at least one edge (u, v) such that dist[v] = dist[u] + w.
    # To maximize the count of good vertices, we should greedily pick edges that connect
    # a vertex u (already reachable with correct distance) to a vertex v (not yet reachable)
    # where dist[v] = dist[u] + w.
    # Since we want to maximize the number of good vertices, and each edge can make at most
    # one new vertex good (the one with larger distance), the optimal strategy is:
    # 1. Process vertices in increasing order of their shortest distance.
    # 2. For each vertex v (starting from the smallest distance > 0), if it hasn't been reached yet,
    #    pick one incoming edge (u, v) such that dist[v] = dist[u] + w.
    #    This edge will make v good.
    # 3. Stop when we have selected k edges or all vertices are processed.
    
    # We need to group edges by the destination vertex v and check if they satisfy the condition.
    # Let's create a list of candidate edges for each vertex v:
    # candidates[v] = list of u such that dist[v] == dist[u] + w(u,v)
    
    candidates = [[] for _ in range(n + 1)]
    
    # We only care about edges where dist[u] != -1 and dist[v] != -1
    # Actually, since the graph is connected and we run Dijkstra from 1, all dists will be valid.
    
    for u, v, w, idx in edges:
        if dist[u] != -1 and dist[v] != -1:
            if dist[v] == dist[u] + w:
                candidates[v].append((u, idx))
            # Note: The graph is undirected, so we also check the reverse direction?
            # The condition for v being reached from u is dist[v] = dist[u] + w.
            # If we consider the edge (v, u) with weight w, then for u to be reached from v:
            # dist[u] == dist[v] + w. This is a different condition.
            # We are building the Shortest Path DAG rooted at 1.
            # An edge (u, v) is in the SP-DAG if dist[v] = dist[u] + w.
            # So for a specific target v, we look for u such that dist[v] = dist[u] + w.
            # The loop above covers all edges. If an edge connects u and v, we check both implications?
            # No, the loop iterates over each edge once.
            # If dist[v] == dist[u] + w, then this edge can be used to reach v from u.
            # If dist[u] == dist[v] + w, then this edge can be used to reach u from v.
            # We need to populate candidates for BOTH v and u if the condition holds for the respective target.
            
            if dist[u] == dist[v] + w:
                candidates[u].append((v, idx))

    # Sort vertices by distance to process in order
    # We only care about vertices with dist > 0 (vertex 1 is already good with 0 edges)
    vertices_by_dist = []
    for i in range(1, n + 1):
        if dist[i] != -1:
            vertices_by_dist.append((dist[i], i))
    
    vertices_by_dist.sort()
    
    selected_edges = []
    good_count = 0
    
    # We iterate through vertices in increasing order of distance.
    # For each vertex v, if it is not yet "good" (i.e., we haven't selected an edge to reach it),
    # we pick one incoming edge from candidates[v].
    # Since we process in increasing order of distance, any u in candidates[v] will have dist[u] < dist[v],
    # so u will have been processed already (or is 1).
    
    # To track which vertices are already good, we can use a boolean array or set.
    # However, note: if we pick an edge to reach v, v becomes good.
    # We stop when we have k edges.
    
    # Optimization: We don't need to check if v is good if we process in order.
    # But wait, multiple vertices might have the same distance.
    # If we have multiple vertices with the same distance, the order between them doesn't matter
    # because they cannot reach each other via shortest path edges (since w >= 1).
    # So processing order among same-distance vertices is arbitrary.
    
    # We need to know if a vertex has been reached.
    reached = [False] * (n + 1)
    reached[1] = True
    
    for d, v in vertices_by_dist:
        if reached[v]:
            continue
        
        # If no incoming shortest path edge exists, this vertex is unreachable in the SP-DAG?
        # But the graph is connected, so there must be at least one.
        if not candidates[v]:
            continue
            
        # Pick the first available edge
        u, idx = candidates[v][0]
        selected_edges.append(idx)
        reached[v] = True
        good_count += 1
        
        if len(selected_edges) == k:
            break
            
    # Output the result
    print(len(selected_edges))
    print(*(selected_edges))

if __name__ == '__main__':
    solve()