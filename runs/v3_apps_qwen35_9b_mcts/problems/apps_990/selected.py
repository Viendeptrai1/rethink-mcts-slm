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
    except StopIteration:
        return

    adj = [[] for _ in range(N + 1)]
    edges = []
    
    # Read N-1 edges
    for _ in range(N - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)
        edges.append((u, v))
    
    try:
        M = int(next(iterator))
    except StopIteration:
        M = 0

    restrictions = []
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        restrictions.append((u, v))

    # Precompute the set of edge indices for each restriction
    # We will map each edge (u, v) to an index 0..N-2
    edge_map = {}
    for idx, (u, v) in enumerate(edges):
        edge_map[(u, v)] = idx
        edge_map[(v, u)] = idx

    # For each restriction, find the path and collect edge indices
    # Since N is small (<=50), we can use BFS/DFS for each restriction
    restriction_edges = []
    
    for u, v in restrictions:
        # BFS to find path
        parent = {u: None}
        queue = [u]
        found = False
        while queue and not found:
            curr = queue.pop(0)
            if curr == v:
                found = True
                break
            for nxt in adj[curr]:
                if nxt not in parent:
                    parent[nxt] = curr
                    queue.append(nxt)
        
        # Reconstruct path
        path_edges = []
        curr = v
        while curr is not None:
            p = parent[curr]
            if p is not None:
                edge_key = (min(curr, p), max(curr, p))
                idx = edge_map[edge_key]
                path_edges.append(idx)
            curr = p
        
        restriction_edges.append(path_edges)

    # Total ways without restrictions is 2^(N-1)
    # We need to count ways where ALL restrictions are satisfied.
    # A restriction is satisfied if at least one edge on its path is BLACK.
    # It is easier to count the complement: ways where at least one restriction is NOT satisfied.
    # However, with M up to 20, inclusion-exclusion over subsets of restrictions is feasible (2^20 ~ 10^6).
    # But the previous reasoning noted that O(2^M * N) might be slow due to set operations.
    # We can optimize by precomputing the union of edges for each subset.
    # Actually, the condition "at least one edge is black" is equivalent to "NOT (all edges are white)".
    # So a subset of restrictions S is "violated" if for every r in S, all edges on r are white.
    # This means the union of edges in S must be white.
    # If we fix a set of edges to be white, we can check if it violates any restriction.
    # But inclusion-exclusion is:
    # Answer = Sum_{S subset of Restrictions} (-1)^|S| * (ways where all r in S are violated)
    # "All r in S are violated" means for every r in S, all edges in r are white.
    # This is equivalent to: all edges in (Union of edges in r for r in S) are white.
    # Let U_S = Union of edges in restrictions in S.
    # If |U_S| = k, then there are 2^(N-1 - k) ways to paint the remaining edges arbitrarily,
    # provided the edges in U_S are forced to be white.
    # So Answer = Sum_{S} (-1)^|S| * 2^(N-1 - |Union(S)|)
    
    # To optimize: many subsets S will have the same Union(S).
    # We can iterate over all possible unions? No, there are 2^(N-1) subsets of edges.
    # But M is small (<=20). We can iterate over all 2^M subsets of restrictions.
    # For each subset, compute the union size.
    # To speed up, we can use a recursive backtracking approach to generate subsets and maintain the current union size.
    
    # Precompute edge sets as bitmasks? N <= 50, so 64-bit integer is sufficient.
    # Python handles large integers automatically.
    
    edge_masks = []
    for r_edges in restriction_edges:
        mask = 0
        for idx in r_edges:
            mask |= (1 << idx)
        edge_masks.append(mask)
    
    total_edges = N - 1
    full_mask = (1 << total_edges) - 1
    
    # We need to compute Sum_{S} (-1)^|S| * 2^(total_edges - popcount(Union(S)))
    # Let's use recursion to iterate subsets of restrictions (0 to M-1)
    # Maintain current union mask and current count of restrictions.
    
    ans = 0
    
    # Recursive function
    # idx: current restriction index being considered
    # current_mask: union of edges for the current subset
    # count: number of restrictions in the current subset
    
    def backtrack(idx, current_mask, count):
        nonlocal ans
        
        # Base case: processed all restrictions
        if idx == M:
            # Calculate contribution
            # Number of free edges = total_edges - popcount(current_mask)
            # But wait, if current_mask has bits set that are not in the tree? 
            # Our masks only use bits 0..N-2, so it's fine.
            # However, we must ensure we don't count edges that don't exist? 
            # The masks are built from valid edge indices 0..N-2.
            
            # Popcount
            # In Python, bin(x).count('1') works
            free_edges = total_edges - bin(current_mask).count('1')
            ways = 1 << free_edges
            
            if count % 2 == 1:
                ans -= ways
            else:
                ans += ways
            return
        
        # Option 1: Do not include restriction idx in the subset S
        # The union mask remains the same, count remains the same.
        # We move to idx+1.
        backtrack(idx + 1, current_mask, count)
        
        # Option 2: Include restriction idx in the subset S
        # Update mask: current_mask | edge_masks[idx]
        # Update count: count + 1
        backtrack(idx + 1, current_mask | edge_masks[idx], count + 1)

    backtrack(0, 0, 0)
    
    print(ans)

if __name__ == '__main__':
    solve()