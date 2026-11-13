import sys

# Increase recursion depth for deep DFS/BFS if necessary, though we will use iterative approaches.
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
    adj = [[] for _ in range(n + 1)]
    
    # Read edges
    for i in range(1, m + 1):
        u = int(next(iterator))
        v = int(next(iterator))
        w = int(next(iterator))
        edges.append((u, v, w, i))
        adj[u].append((v, w, i))
        adj[v].append((u, w, i))

    # Step 1: Compute shortest path distances from vertex 1 using Dijkstra
    INF = float('inf')
    dist = [INF] * (n + 1)
    dist[1] = 0
    
    # Priority queue: (distance, vertex)
    import heapq
    pq = [(0, 1)]
    
    while pq:
        d, u = heapq.heappop(pq)
        
        if d > dist[u]:
            continue
        
        for v, w, _ in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))

    # Step 2: Build the Shortest Path DAG and compute in-degrees
    # An edge (u, v) with weight w is part of a shortest path tree if dist[u] + w == dist[v] (or vice versa)
    # We need to select at most k edges to cover the maximum number of vertices (excluding 1).
    # Since it's an unweighted selection problem on a DAG structure where each node needs 1 incoming edge from a "shorter" node:
    # We can model this as: each node v (v != 1) needs exactly one incoming edge from a parent u such that dist[u] + w = dist[v].
    # We want to pick a set of edges E' (|E'| <= k) such that the number of reachable nodes from 1 in the subgraph (restricted to edges in E' that are on shortest paths) is maximized.
    # Actually, the condition "path exists" means in the subgraph of kept edges, there is a path 1->v.
    # If we keep an edge (u, v) on a shortest path, it helps connect v only if u is also connected.
    # This looks like we are selecting a subgraph of the SP-DAG.
    # To maximize good vertices with <= k edges:
    # We should greedily pick edges that connect new vertices.
    # Specifically, if we process vertices in increasing order of their shortest distance (which corresponds to topological order of SP-DAG),
    # for each vertex v, we can choose one incoming edge (u, v) that is on a shortest path.
    # If we choose this edge, and u is already "good" (connected to 1), then v becomes good.
    # Since we process by distance, u will always have dist[u] <= dist[v].
    # If dist[u] == dist[v], then w=0. But weights are >= 1, so dist[u] < dist[v] strictly for any edge on a shortest path (since w >= 1).
    # So strict topological order exists.
    # Strategy:
    # 1. Group vertices by their distance.
    # 2. Iterate through groups from smallest distance to largest.
    # 3. For each vertex v in current group, identify all incoming edges (u, v) on shortest paths.
    # 4. Among these, pick one edge (u, v) such that u is already good.
    #    If multiple such u exist, it doesn't matter which one we pick for connectivity of v, 
    #    BUT we need to be careful: picking an edge costs 1 from our budget k.
    #    The goal is to maximize the count of good vertices.
    #    Since every vertex v (except 1) requires at least 1 edge to be good, and edges are shared?
    #    No, in a DAG, edges are distinct. To make v good, we MUST include at least one edge entering v.
    #    Can one edge make two vertices good? No, an edge has one target.
    #    So each good vertex (except 1) consumes exactly 1 edge from our budget.
    #    Therefore, the maximum number of good vertices we can get is simply min(n-1, k), 
    #    PROVIDED we can actually find a parent for every vertex within the budget.
    #    Wait, is it always possible to find a parent?
    #    Yes, because the original graph is connected and we computed shortest paths. Every v != 1 has at least one parent u with dist[u] + w = dist[v].
    #    So we can always pick a parent.
    #    The constraint is simply: we have k edges. Each good vertex v != 1 needs 1 edge.
    #    So we can save k-1 edges (if k >= n-1, we save all n-1 edges, count = n).
    #    If k < n-1, we can save k edges, count = k+1 (including vertex 1).
    #    
    #    Is there any catch? 
    #    "Good if there still exists a path".
    #    If we pick edges {(u1, v1), (u2, v2), ...}, vertex v is good if 1 -> ... -> u -> v exists.
    #    Since we process in topological order (by distance), if we ensure that for every selected edge (u, v), u is good, then v becomes good.
    #    Base case: 1 is good.
    #    Step: Pick (u, v). u is good (by induction or base case). Then v is good.
    #    Cost: 1 edge per new good vertex.
    #    Total good vertices = 1 + (number of edges picked).
    #    Max edges = k.
    #    Max good vertices = 1 + k (capped at n).
    #    
    #    So the algorithm is trivial:
    #    We need to output ANY set of min(n-1, k) edges that form a valid shortest path tree structure (or forest rooted at 1) covering 1 + min(n-1, k) nodes.
    #    Actually, we just need to pick min(n-1, k) edges such that they connect 1 to some other nodes via shortest paths.
    #    Greedy approach:
    #    Sort vertices by distance.
    #    Maintain a set of "good" vertices (initially {1}).
    #    For each vertex v (in sorted order, skipping 1):
    #        Find an incoming edge (u, v) on a shortest path where u is good.
    #        If we still have edges left in our budget (count < k):
    #            Add this edge to our result.
    #            Mark v as good.
    #            Increment count.
    #        Else:
    #            Stop (or continue to fill if we want exactly k, but problem says "at most k").
    #            Actually, we stop adding edges once we hit k, but we might skip some vertices if we run out of edges.
    #            The problem asks to maximize good vertices. Since each edge adds exactly 1 good vertex (the target), 
    #            and we start with 1, the max is 1 + min(n-1, k).
    #            We just need to output the edges.
    
    # Implementation details:
    # 1. Create a list of vertices 2..n with their distances.
    # 2. Sort by distance.
    # 3. Maintain a set `good` = {1}.
    # 4. For each v in sorted list:
    #      Find an edge (u, v, w, idx) such that dist[u] + w == dist[v] AND u in good.
    #      If we can find such an edge and len(result_edges) < k:
    #          Add idx to result_edges.
    #          Add v to good.
    #          Break inner loop (move to next v).
    
    # Optimization: 
    # To efficiently find a parent u for v that is already good:
    # We can iterate over all incoming edges of v on shortest paths.
    # Since the graph can be dense, iterating all incoming edges for every node might be O(m) total if we are careful, 
    # but in worst case (all edges on SP-DAG) it could be O(m). Given m=3*10^5, O(m) is fine.
    # We just need to store incoming edges on shortest paths.
    
    # Precompute incoming edges for shortest paths
    # incoming[v] = list of (u, w, edge_index) such that dist[u] + w == dist[v]
    incoming = [[] for _ in range(n + 1)]
    
    for u, v, w, idx in edges:
        # Check u -> v
        if dist[u] != INF and dist[u] + w == dist[v]:
            incoming[v].append((u, w, idx))
        # Check v -> u
        if dist[v] != INF and dist[v] + w == dist[u]:
            incoming[u].append((v, w, idx))
            
    # Sort vertices by distance
    # We only care about vertices 2..n
    vertices_by_dist = []
    for i in range(2, n + 1):
        if dist[i] != INF:
            vertices_by_dist.append(i)
    
    vertices_by_dist.sort(key=lambda x: dist[x])
    
    good_set = {1}
    result_indices = []
    edges_count = 0
    
    for v in vertices_by_dist:
        if edges_count >= k:
            break
            
        # Find a parent u that is already good
        parent_found = False
        for u, w, idx in incoming[v]:
            if u in good_set:
                # Found a valid parent
                result_indices.append(idx)
                good_set.add(v)
                edges_count += 1
                parent_found = True
                break
        
        # Note: It is guaranteed that at least one parent exists in the original SP-DAG.
        # However, it is possible that all parents are NOT yet in good_set?
        # Since we process in increasing order of distance, and w >= 1, dist[u] < dist[v].
        # So u appears earlier in the sorted list.
        # If u was reachable via shortest path from 1 in the original graph, then u would have been processed.
        # But u might not be "good" if we ran out of edges for u?
        # Wait. If u is not in good_set, it means we skipped u (didn't pick an edge for u) because we ran out of edges earlier.
        # If we ran out of edges for u, we cannot pick an edge for v either (since we are at limit k).
        # So if edges_count >= k, we break anyway.
        # If edges_count < k, then we haven't reached the limit yet.
        # Does a valid parent u always exist in good_set?
        # Not necessarily. Example: 1->2 (cost 10), 1->3 (cost 10), 2->4 (cost 1), 3->4 (cost 1).
        # Distances: 1:0, 2:10, 3:10, 4:11.
        # Sorted: 2, 3, 4.
        # Process 2: Parent 1 (good). Pick edge (1,2). good={1,2}. count=1.
        # Process 3: Parent 1 (good). Pick edge (1,3). good={1,2,3}. count=2.
        # Process 4: Parents 2 (good), 3 (good). Pick one.
        # What if we skipped 2?
        # Suppose k=1.
        # Process 2: Pick (1,2). count=1. Break loop.
        # Result: 1 edge. Good vertices: {1, 2}.
        # Process 3: Skipped.
        # Process 4: Skipped.
        # Is it possible that for v, all parents u are NOT in good_set?
        # Only if we skipped u. But if we skipped u, it means we reached k edges before processing u (or u was processed but we didn't pick an edge? No, we pick if we can).
        # Actually, we iterate v in order.
        # If we have budget, we pick for v.
        # The only risk is if all parents u of v were skipped.
        # When would u be skipped? Only if we ran out of edges before processing u.
        # But if we ran out of edges before processing u, we definitely ran out of edges before processing v (since u comes before v).
        # So if edges_count < k, then we haven't reached the limit yet.
        # Could it be that we skipped u even though we had budget?
        # No, because for u, we check its parents. Since u comes before v, and parents of u have smaller distance, they were processed earlier.
        # By induction, if we have budget, every node processed so far (and eligible) will be added.
        # Wait, is it possible that u has NO parents in good_set?
        # Base case: 1 is good.
        # For any v, let P(v) be the set of parents on SP-DAG.
        # Since dist[u] < dist[v] for all u in P(v), u appears before v.
        # If u was processed and we had budget, u was added to good_set.
        # If u was processed and we did NOT have budget, then we broke the loop and didn't process v anyway.
        # So if we are processing v and edges_count < k, it implies we didn't break the loop earlier.
        # This implies for all previous nodes x, we had budget and picked an edge?
        # Yes, because the loop condition `if edges_count >= k: break` is checked at the start of each iteration.
        # So if we are at v and count < k, then for all u processed before v, we successfully picked an edge (unless u had no good parents? But 1 is good, so root nodes have good parents).
        # Thus, every u processed before v is in good_set.
        # Since all parents u of v have dist[u] < dist[v], they were all processed before v.
        # Therefore, ALL parents of v are in good_set.
        # So we just need to pick ANY parent.
        # We don't need to search for a "good" parent specifically; any parent will do, and it will be good.
        
        # Re-verification:
        # Is it possible that u was processed but we didn't pick an edge for u?
        # Only if we ran out of edges. But if we ran out of edges, we break the outer loop.
        # So if we are inside the loop for v, we haven't run out of edges.
        # So we must have picked edges for all previous vertices.
        # Correct.
        
        # So the logic simplifies to:
        # For each v in sorted order:
        #   Pick first available edge (u, v) on SP-DAG.
        #   Add to result.
        #   Increment count.
        #   Stop if count == k.
        
        # Wait, is it possible that u was NOT processed?
        # We sort by distance. u has dist[u] < dist[v]. So u is strictly before v in the list.
        # So u is processed.
        # So yes, u is in good_set.
        
        # One edge case: Multiple edges between u and v? Problem says simple graph.
        # Multiple paths? We just need one edge.
        
        # So the code is:
        # for v in sorted_vertices:
        #     if count == k: break
        #     pick any (u, w, idx) from incoming[v]
        #     add idx
        #     count++
    
    # Let's refine the loop to be absolutely safe.
    # We will just pick the first available incoming edge.
    
    for v in vertices_by_dist:
        if len(result_indices) == k:
            break
        
        # Find any parent
        # Since we proved all parents are good, we just need one.
        found = False
        for u, w, idx in incoming[v]:
            # Just pick the first one.
            result_indices.append(idx)
            good_set.add(v) # Technically redundant for logic, but good for tracking
            found = True
            break
        
        # It is guaranteed that incoming[v] is not empty for v != 1 in a connected graph with positive weights.
        # dist[v] = min(dist[u] + w). Since graph connected, such u exists.
        
    # Output
    print(len(result_indices))
    print(*(result_indices))

if __name__ == '__main__':
    solve()