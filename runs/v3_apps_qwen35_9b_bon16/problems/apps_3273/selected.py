import sys

def solve():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    
    try:
        n = int(input_data[0].strip())
    except ValueError:
        return
    
    fragments = []
    for i in range(1, n + 1):
        fragments.append(input_data[i])
    
    # Build adjacency list: for each fragment u, find all v that can follow u
    # Condition: suffix of u (len >= 5) == prefix of v, and overlap is maximal for that pair
    # Also, given the problem constraints, there is exactly one way two compatible fragments overlap.
    # We need to find the path that maximizes the number of fragments.
    
    # Since n is small (<= 250), we can try to model this as a DAG and find the longest path.
    # However, the graph might not be a simple DAG initially if we don't check cycles carefully, 
    # but the problem guarantees no cycles exist in valid chains of length >= 2.
    # Also, we need to check for ambiguity.
    
    # Let's define the overlap function:
    # Given u and v, find the longest k >= 5 such that u[-k:] == v[:k].
    # If no such k exists, overlap is 0.
    
    def get_overlap(u, v):
        max_len = min(len(u), len(v))
        # Check from longest possible down to 5
        for k in range(max_len, 4, -1):
            if u[-k:] == v[:k]:
                return k
        return 0

    # Build graph
    # nodes are indices 0 to n-1
    # edges (u, v) exist if overlap(u, v) >= 5
    # Since the problem states "exactly one way", if multiple k work, the largest k is the intended one?
    # Actually, the problem says "whenever fragment A immediately precedes fragment B: A has a suffix ... equal to a prefix of B ... shared length at least 5".
    # It also says "two fragments that satisfy these criteria do so in exactly one way". This implies for any pair (u, v), there is at most one valid overlap length >= 5, or if there are multiple k, the condition implies a unique physical placement? 
    # Re-reading: "It is guaranteed that two fragments that satisfy these criteria do so in exactly one way."
    # This likely means for any pair u, v, there is either 0 or 1 valid overlap length >= 5.
    # So we just check if any k >= 5 exists. If so, that's the overlap.
    
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            ov = get_overlap(fragments[i], fragments[j])
            if ov >= 5:
                adj[i].append(j)
    
    # We need to find a path in this DAG that visits the maximum number of nodes.
    # Since n is small (250), and the graph is guaranteed acyclic for valid sequences, we can use DFS with memoization.
    # However, we also need to detect ambiguity. Ambiguity occurs if there are two different maximal-length paths.
    # Note: The problem says "no fragment is contained within another fragment". This simplifies things as we don't have subgraph issues.
    # Also "no sequence ... forms a cycle". So it's a DAG.
    
    # Algorithm:
    # 1. Compute longest path ending at each node and count how many such paths exist.
    # 2. Find the global maximum length.
    # 3. Count how many paths have this length.
    # 4. If count == 1, reconstruct the unique path. Else, output AMBIGUOUS.
    
    # Since the graph is a DAG, we can compute DP.
    # dp[u] = (max_len_from_u, count_of_max_len_paths_from_u)
    # But we need to consider starting points. Any node can be a start.
    # Actually, we want the longest path in the entire graph.
    # Let's compute longest path starting from each node.
    
    # dp[u] = (length, count)
    # length = 1 + max(dp[v].length for v in adj[u])
    # count = sum(dp[v].count for v in adj[u] where dp[v].length is max)
    # Base case: leaf nodes have length 1, count 1.
    
    # We need to handle the case where a node has no outgoing edges.
    
    # Memoization table
    memo_len = {}
    memo_count = {}
    
    def get_dp(u):
        if u in memo_len:
            return memo_len[u], memo_count[u]
        
        # Find best neighbor
        best_l = -1
        best_c = 0
        
        candidates = []
        for v in adj[u]:
            l, c = get_dp(v)
            if l > best_l:
                best_l = l
                best_c = c
                candidates = [(v, l, c)]
            elif l == best_l:
                candidates.append((v, l, c))
        
        if not candidates:
            # Leaf node
            res_len = 1
            res_count = 1
        else:
            res_len = 1 + best_l
            res_count = sum(c for _, _, c in candidates)
        
        memo_len[u] = res_len
        memo_count[u] = res_count
        return res_len, res_count

    # Compute for all nodes
    all_lens = []
    all_counts = []
    for i in range(n):
        l, c = get_dp(i)
        all_lens.append(l)
        all_counts.append(c)
    
    max_len = max(all_lens)
    
    # Count total number of maximal paths
    total_max_paths = 0
    for i in range(n):
        if all_lens[i] == max_len:
            total_max_paths += all_counts[i]
    
    if total_max_paths > 1:
        print("AMBIGUOUS")
        return
    
    # Reconstruct the unique path
    # Start from the node(s) that achieve max_len
    start_nodes = [i for i in range(n) if all_lens[i] == max_len]
    
    # There should be exactly one start node for a unique path
    if len(start_nodes) != 1:
        # This shouldn't happen if total_max_paths == 1, but just in case
        print("AMBIGUOUS")
        return
    
    start_node = start_nodes[0]
    current = start_node
    path_indices = [current]
    
    # Trace back forward
    # We need to make greedy choices based on the DP table
    while True:
        # Find neighbors that lead to the optimal path
        next_candidates = []
        for v in adj[current]:
            l, _ = get_dp(v)
            if 1 + l == all_lens[current]:
                next_candidates.append(v)
        
        if len(next_candidates) != 1:
            # Should not happen if path is unique
            print("AMBIGUOUS")
            return
        
        current = next_candidates[0]
        path_indices.append(current)
        
        if not adj[current]:
            break
    
    # Reconstruct the string
    # F1 || omega(F2) || ...
    # omega(Fi) = Fi without the prefix of length 'overlap'
    
    result_parts = []
    result_parts.append(fragments[path_indices[0]])
    
    for i in range(1, len(path_indices)):
        prev_idx = path_indices[i-1]
        curr_idx = path_indices[i]
        overlap_len = get_overlap(fragments[prev_idx], fragments[curr_idx])
        
        # Remove prefix of length overlap_len from current fragment
        # The problem says: "removing the prefix of length >= 5 that is equal to a suffix of F_{i-1}"
        # Since overlap_len is the length of the matching suffix/prefix, we remove exactly that many chars from the start of curr.
        # Wait, the definition: "omega(Fi) is the substring of Fi obtained by removing the prefix of length >= 5 that is equal to a suffix of F_{i-1}"
        # Yes, remove overlap_len characters from the beginning of fragments[curr_idx].
        
        suffix_to_add = fragments[curr_idx][overlap_len:]
        result_parts.append(suffix_to_add)
    
    print("".join(result_parts))

if __name__ == "__main__":
    solve()