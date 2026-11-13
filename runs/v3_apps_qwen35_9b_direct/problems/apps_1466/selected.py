import sys

# Increase recursion depth just in case, though we will use iterative BFS/Dijkstra
sys.setrecursionlimit(400000)

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

    edges = []
    for i in range(m):
        u = int(next(iterator))
        v = int(next(iterator))
        w = int(next(iterator))
        edges.append((u, v, w, i + 1))  # Store 1-based index

    # Build adjacency list for Dijkstra
    adj = [[] for _ in range(n + 1)]
    for idx, (u, v, w, _) in enumerate(edges):
        adj[u].append((v, w, idx))
        adj[v].append((u, w, idx))

    # Dijkstra's algorithm to find shortest distances from vertex 1
    import heapq
    dist = [-1] * (n + 1)
    dist[1] = 0
    pq = [(0, 1)]
    
    while pq:
        d, u = heapq.heappop(pq)
        
        if dist[u] != -1 and d > dist[u]:
            continue
        
        for v, w, _ in adj[u]:
            if dist[v] == -1 or dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))

    # Now we need to select at most k edges to maximize the number of "good" vertices.
    # A vertex i is good if there is a path from 1 to i with length d_i using the selected edges.
    # This means we need to form a subgraph containing a shortest path tree (or forest rooted at 1)
    # that covers as many vertices as possible, using at most k edges.
    #
    # Strategy:
    # 1. Identify all edges that can be part of a shortest path. An edge (u, v) with weight w
    #    is a shortest-path edge if dist[u] + w == dist[v] (and similarly for v to u).
    # 2. Among these valid edges, we want to pick a set that forms a tree (or forest) rooted at 1
    #    covering the maximum number of vertices, with size <= k.
    # 3. Since we want to maximize vertices, and each edge in a tree adds exactly one new vertex (except the root),
    #    we should greedily pick edges that lead to vertices with the smallest "cost" to include? 
    #    Actually, in a shortest path DAG, every vertex (except 1) has at least one incoming edge from a vertex
    #    with a strictly smaller distance. To cover a vertex v, we must include at least one incoming shortest-path edge.
    #    To maximize vertices with <= k edges, we should pick the k edges that allow us to reach the most vertices.
    #    However, simply picking any k edges might not form a connected component from 1.
    #
    # Refined Strategy:
    # We can view this as: we have a DAG of shortest path edges. We want to select a subset of edges
    # such that the number of reachable vertices from 1 is maximized, subject to |E'| <= k.
    # Note: If we select a set of edges that forms a tree rooted at 1, the number of reachable vertices is |E'| + 1.
    # So maximizing vertices is equivalent to maximizing edges, up to k.
    # BUT, we cannot just pick any k edges; they must be connected to 1.
    #
    # Observation:
    # If we decide to include a vertex v in our set of good vertices, we must include at least one incoming
    # shortest-path edge to v. If we include multiple vertices, we need to ensure connectivity to 1.
    # The optimal structure is always a tree (or a set of trees connected to 1, which is just one tree if connected).
    # Actually, since the graph is connected and we only care about reachability from 1, the optimal set of edges
    # will form a tree rooted at 1 (if we want to maximize vertices for a given number of edges).
    #
    # So the problem reduces to: Select at most k edges from the shortest-path DAG such that they form a tree
    # rooted at 1 and cover the maximum number of vertices.
    # Since a tree with e edges covers e+1 vertices, maximizing vertices is equivalent to maximizing edges,
    # provided the edges form a valid tree.
    #
    # Can we always form a tree with k edges? Yes, if there are at least k vertices reachable via shortest paths
    # (which is all vertices since the graph is connected).
    # We just need to pick k edges that form a tree. Any tree with k edges has k+1 vertices.
    # So if we can pick k edges that form a tree, we get k+1 good vertices.
    # Is it possible that we can't form a tree with k edges? Only if the total number of shortest-path edges
    # available to form a spanning tree is less than k? But the shortest path DAG always contains a spanning tree
    # of all n vertices (since the graph is connected). The number of edges in a spanning tree is n-1.
    # If k >= n-1, we can keep n-1 edges and get n good vertices.
    # If k < n-1, we can keep k edges and get k+1 good vertices.
    #
    # Wait, is it that simple?
    # Let's re-read carefully: "maximize the number of good vertices".
    # If we pick k edges that form a tree, we get k+1 vertices.
    # Can we get more than k+1 vertices with k edges? No, because a connected component with V vertices has at least V-1 edges.
    # So V <= E + 1. Thus, with E=k, max V = k+1.
    #
    # Therefore, the strategy is:
    # 1. If k >= n-1, we can keep n-1 edges that form a shortest path tree (spanning all vertices). Answer: n-1 edges, n good vertices.
    # 2. If k < n-1, we need to pick k edges that form a tree rooted at 1. Any k edges from the shortest path DAG that form a tree will do.
    #    We can simply run a BFS/DFS on the shortest path DAG starting from 1 and pick the first k edges encountered that connect to a new vertex.
    #
    # Algorithm:
    # 1. Compute shortest distances (done).
    # 2. Build the DAG of shortest path edges: edge (u, v) with weight w is valid if dist[u] + w == dist[v].
    # 3. Perform a traversal (BFS or DFS) from vertex 1 using only valid edges.
    # 4. Count how many edges we can pick to form a tree. We stop when we have picked k edges or we run out of new vertices.
    #    Since we want a tree, we only add an edge if it leads to a vertex not yet visited in our traversal.
    # 5. Output the selected edges.

    # Step 2 & 3 combined: BFS on shortest path DAG
    visited = [False] * (n + 1)
    visited[1] = True
    selected_edges = []
    
    # We need to traverse the DAG. Since it's a DAG (distances strictly increase), BFS works fine.
    # Queue stores (u, edge_index_from_parent) but we just need to iterate neighbors.
    # Actually, we just need to find k edges that connect unvisited nodes.
    
    queue = [1]
    idx = 0
    while idx < len(queue) and len(selected_edges) < k:
        u = queue[idx]
        idx += 1
        
        for v, w, edge_idx in adj[u]:
            # Check if this is a shortest path edge
            if dist[v] == -1:
                continue
            if dist[u] + w == dist[v]:
                if not visited[v]:
                    visited[v] = True
                    selected_edges.append(edge_idx)
                    queue.append(v)
                    if len(selected_edges) == k:
                        break
        if len(selected_edges) == k:
            break

    # If we couldn't pick k edges (e.g., k is large but we only have n-1 possible in a tree),
    # the loop condition `len(selected_edges) < k` handles it, but we might stop early if we run out of vertices.
    # However, since the graph is connected, we can always reach all n vertices via shortest paths.
    # The maximum number of edges we can pick in a tree is n-1.
    # So if k >= n-1, we will pick n-1 edges and stop because we visited all vertices.
    # The problem says "at most k edges", so picking n-1 when k >= n-1 is valid.
    
    # Output results
    print(len(selected_edges))
    print(*(selected_edges))

if __name__ == '__main__':
    solve()