import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        adj = [[] for _ in range(N + 1)]
        for _ in range(N - 1):
            u = int(next(iterator))
            v = int(next(iterator))
            adj[u].append(v)
            adj[v].append(u)
        
        M = int(next(iterator))
        restrictions = []
        for _ in range(M):
            u = int(next(iterator))
            v = int(next(iterator))
            restrictions.append((u, v))
    except StopIteration:
        return

    # Precompute LCA and path edges using DFS
    parent = [0] * (N + 1)
    depth = [0] * (N + 1)
    edge_from = [0] * (N + 1)  # edge_from[u] = index of edge connecting u to parent[u]
    
    # Map edge (u,v) to an index 0..N-2. We can store edges in a list and identify by index later.
    # Let's store edges as (u, v, index) in adj temporarily or build a mapping.
    # Actually, let's build edge index map: edge_index[u][v] -> index? Too sparse maybe.
    # Better: during DFS, assign edge index to the child node.
    # Edge list:
    edges = []
    
    # Build edge index mapping for quick lookup if needed, but since N is small (50), we can just iterate.
    # However, to efficiently count "all white" configurations, we need to know which edges are on the path.
    # Let's assign each edge an ID from 0 to N-2.
    edge_id_map = {} # (u, v) -> id (undirected)
    current_id = 0
    for u in range(1, N + 1):
        for v in adj[u]:
            if u < v:
                edge_id_map[(u, v)] = current_id
                edges.append((u, v))
                current_id += 1
    
    # Now run DFS to compute parents, depths, and which edge connects a node to its parent
    stack = [(1, 0, 0)] # node, parent, depth
    # Re-run BFS/DFS to set up structure
    parent = [0] * (N + 1)
    depth = [0] * (N + 1)
    edge_to_parent = [0] * (N + 1) # edge_to_parent[u] = edge index connecting u to parent
    
    # Reset visited implicitly by tree structure
    parent[1] = 0
    depth[1] = 0
    
    queue = [1]
    order = []
    while queue:
        u = queue.pop(0)
        order.append(u)
        for v in adj[u]:
            if v != parent[u]:
                parent[v] = u
                depth[v] = depth[u] + 1
                edge = (min(u, v), max(u, v))
                edge_to_parent[v] = edge_id_map[edge]
                queue.append(v)
    
    # Function to get all edge indices on the path between u and v
    def get_path_edges(u, v):
        path = []
        while u != v:
            if depth[u] < depth[v]:
                u, v = v, u
            # Move u up
            edge_idx = edge_to_parent[u]
            path.append(edge_idx)
            u = parent[u]
        return path

    # For each restriction, collect the set of edge indices that must NOT be all white.
    # Actually, the condition is: path contains at least one black edge.
    # Equivalent to: NOT (all edges on path are white).
    # We want to count colorings where for all restrictions, the path is not all white.
    # Total colorings = 2^(N-1).
    # It's easier to count the complement? No, intersections of "not all white" are complex.
    # But N is very small (50), and M is small (20).
    # However, 2^49 is too big for direct enumeration.
    # This suggests an inclusion-exclusion principle or dynamic programming on subsets of restrictions.
    # Since M <= 20, 2^M = 2^20 approx 10^6, which is feasible.
    # Inclusion-Exclusion:
    # Count = Sum_{S subset of Restrictions} (-1)^|S| * Count(colorings where ALL restrictions in S are VIOLATED)
    # A restriction i is violated if ALL edges on path(u_i, v_i) are WHITE.
    # If we fix a set S of restrictions to be violated, then for every restriction in S, all edges on its path must be white.
    # This implies a set of edges must be white. Let U_S be the union of all edges in paths of restrictions in S.
    # If U_S has k edges, then these k edges MUST be white. The remaining (N-1) - k edges can be anything (2^(N-1-k) ways).
    # So Count(S) = 2^(N-1 - |Union of edges in S|).
    # If the union of edges creates a conflict? No, "must be white" constraints are consistent.
    # So we just need to compute the size of the union of edges for each subset S.
    
    # Precompute edges for each restriction
    restriction_edges = []
    for i in range(M):
        u, v = restrictions[i]
        path_edges = get_path_edges(u, v)
        restriction_edges.append(path_edges)
    
    # Map edge index to a bit? No, N is 50, can't use bitmask for edges.
    # But we only need the count of unique edges in the union.
    # We can use a Python set for each subset.
    
    # Optimization: M is up to 20. 2^20 iterations. Inside, we compute union size.
    # To make it faster, we can represent the union as a frozenset or just a set.
    # With N=50, set operations are fast enough for 10^6 iterations?
    # 10^6 * (average path length ~ 25) might be slow in Python (25 million ops).
    # Let's try to optimize.
    # We can precompute the bitmasks for edges if N <= 60? N=50 fits in 64-bit integer.
    # Yes! We can represent the set of edges as a 64-bit integer (or Python int).
    # Then union is bitwise OR. Popcount gives the size.
    
    # Map edge index to bit position
    edge_to_bit = [0] * N # N edges max
    for idx in range(len(edges)):
        edge_to_bit[idx] = 1 << idx
    
    # Precompute mask for each restriction
    restriction_masks = []
    for edges_list in restriction_edges:
        mask = 0
        for e_idx in edges_list:
            mask |= (1 << e_idx)
        restriction_masks.append(mask)
    
    total_edges = N - 1
    total_colorings = 1 << total_edges
    
    # Inclusion-Exclusion
    # Iterate over all masks from 0 to 2^M - 1
    # If popcount(mask) is odd, subtract count. If even, add count.
    # Actually formula: Sum (-1)^|S| * 2^(total_edges - |union(S)|)
    # Let k = |S|. If k is odd, subtract. If even, add.
    
    ans = 0
    limit = 1 << M
    
    # To speed up, we can iterate and maintain union? No, subsets are arbitrary.
    # But 2^20 is 1,048,576. Doing a loop with bitwise ORs and popcounts is very fast in Python.
    
    for s in range(limit):
        # Calculate union of masks in subset s
        union_mask = 0
        for i in range(M):
            if (s >> i) & 1:
                union_mask |= restriction_masks[i]
        
        # Count set bits in union_mask
        # bin(union_mask).count('1') is fast enough for 50 bits
        # Or use bit_count() in Python 3.10+
        if hasattr(int, "bit_count"):
            union_size = union_mask.bit_count()
        else:
            union_size = bin(union_mask).count('1')
        
        ways = 1 << (total_edges - union_size)
        
        # Determine sign
        # Number of set bits in s
        if hasattr(int, "bit_count"):
            k = s.bit_count()
        else:
            k = bin(s).count('1')
        
        if k % 2 == 1:
            ans -= ways
        else:
            ans += ways
            
    print(ans)

if __name__ == '__main__':
    solve()