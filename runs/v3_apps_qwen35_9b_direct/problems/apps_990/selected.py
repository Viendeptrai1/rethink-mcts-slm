import sys

# Increase recursion depth just in case, though N is small.
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        edges = []
        adj = [[] for _ in range(N + 1)]
        
        for _ in range(N - 1):
            u = int(next(iterator))
            v = int(next(iterator))
            edges.append((u, v))
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

    # Precompute the set of edges on the path between u and v for each restriction
    # We will represent each edge by its index (0 to N-2)
    
    # BFS/DFS to find path between two nodes and collect edge indices
    def get_path_edges(u, v):
        parent = {u: None}
        edge_from_parent = {u: -1}
        queue = [u]
        
        while queue:
            curr = queue.pop(0)
            if curr == v:
                break
            for nxt in adj[curr]:
                if nxt not in parent:
                    parent[nxt] = curr
                    edge_from_parent[nxt] = edge_from_parent[curr] # This is wrong logic, need to store edge index
                    # Let's redo with edge index storage
                    pass
        
        # Redo BFS properly storing edge indices
        parent_node = {u: None}
        edge_idx = {u: -1}
        queue = [u]
        
        while queue:
            curr = queue.pop(0)
            if curr == v:
                break
            for i, nxt in enumerate(adj[curr]):
                if nxt not in parent_node:
                    parent_node[nxt] = curr
                    edge_idx[nxt] = i
                    queue.append(nxt)
        
        # Reconstruct path
        path_indices = []
        curr = v
        while curr != u:
            path_indices.append(edge_idx[curr])
            curr = parent_node[curr]
        
        return path_indices

    # For each restriction, get the list of edge indices that must contain at least one black edge
    # Let S_i be the set of edge indices for restriction i.
    # Condition: NOT (all edges in S_i are white)
    # Total ways = Sum over all subsets of edges being white of:
    #   (-1)^|intersection of constraints violated| ? 
    # Actually, let's use Inclusion-Exclusion Principle on the "bad" sets.
    # A configuration is bad if it violates at least one restriction.
    # Let P_i be the property that restriction i is violated (i.e., all edges in S_i are white).
    # We want Total - |Union(P_i)|.
    # By PIE: |Union(P_i)| = Sum |P_i| - Sum |P_i and P_j| + ...
    # |P_{i1} and ... and P_{ik}| means all edges in (S_{i1} U ... U S_{ik}) are white.
    # If the union of edge sets has size k, then there are 2^(N-1 - k) ways to paint the rest.
    
    # Since M is small (<= 20), we can iterate over all non-empty subsets of restrictions.
    # There are 2^M - 1 subsets. 2^20 is about 10^6, which is feasible.
    
    M_list = list(range(M))
    total_edges = N - 1
    
    # Precompute edge sets for each restriction
    restriction_edge_sets = []
    for i in range(M):
        u, v = restrictions[i]
        path = get_path_edges(u, v)
        restriction_edge_sets.append(set(path))
    
    # Iterate over all non-empty subsets of restrictions using bitmask
    # We want to calculate Sum_{non-empty S subset of {0..M-1}} (-1)^(|S|-1) * 2^(total_edges - |Union_{i in S} S_i|)
    # Then Answer = 2^(total_edges) - |Union| = 2^(total_edges) - (Sum ... with alternating signs starting with + for size 1)
    # Wait, standard PIE for Union:
    # |Union| = S1 - S2 + S3 - ... where Sk is sum of intersections of k sets.
    # So |Union| = Sum_{k=1 to M} (-1)^(k-1) * (sum of ways where specific k restrictions are violated)
    # Ways where specific k restrictions are violated = 2^(total_edges - |Union of their edge sets|)
    # So Answer = Total - |Union| = 2^T - [ Sum_{k=1} (-1)^(k-1) * Count_k ]
    #          = 2^T + Sum_{k=1} (-1)^k * Count_k
    #          = Sum_{k=0} (-1)^k * Count_k  (where Count_0 = 2^T, k=0 term)
    
    # So we just iterate all masks from 1 to 2^M - 1.
    # Let k = popcount(mask).
    # Term = (-1)^k * 2^(total_edges - |union of edges in mask|)
    # Add this to the total sum.
    # Finally, the result is the sum.
    
    # Optimization: Since N is small (50), total_edges <= 49.
    # We can compute union size efficiently.
    
    import itertools
    
    # Precompute edge sets as bitmasks? N-1 <= 49, so we need 64-bit integers. Python handles large ints automatically.
    # This will make union computation very fast (bitwise OR).
    
    edge_masks = []
    for i in range(total_edges):
        edge_masks.append(1 << i)
        
    restriction_masks = []
    for s in restriction_edge_sets:
        mask = 0
        for idx in s:
            mask |= edge_masks[idx]
        restriction_masks.append(mask)
        
    total_ways = 1 << total_edges
    ans = 0
    
    # Iterate all non-empty subsets of restrictions
    # Since M <= 20, 2^20 = 1,048,576. Loop is fine.
    num_subsets = 1 << M
    for mask in range(1, num_subsets):
        # Calculate union of edge masks for this subset
        union_mask = 0
        count_restrictions = 0
        
        # Iterate bits of mask
        temp = mask
        idx = 0
        while temp > 0:
            if temp & 1:
                union_mask |= restriction_masks[idx]
                count_restrictions += 1
            temp >>= 1
            idx += 1
            
        # Number of edges that MUST be white is the number of set bits in union_mask
        forced_white_count = bin(union_mask).count('1')
        
        # Ways to paint remaining edges: 2^(total_edges - forced_white_count)
        ways = 1 << (total_edges - forced_white_count)
        
        # Add to answer with sign (-1)^count_restrictions
        if count_restrictions % 2 == 1:
            ans += ways
        else:
            ans -= ways
            
    print(ans)

if __name__ == '__main__':
    solve()