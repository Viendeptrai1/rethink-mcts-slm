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
        fragments.append(input_data[i].strip())

    # Build a directed graph where an edge exists from A to B if A can precede B
    # with overlap >= 5.
    # Since the problem guarantees uniqueness of overlap for any pair, we don't need to worry about multiple edges.
    
    # We need to find a path that visits the maximum number of nodes (fragments).
    # Constraints: n <= 250. This suggests an algorithm better than exponential, likely O(n^3) or O(n^4).
    # Since it's a path finding problem on a DAG (guaranteed no cycles), we can use dynamic programming.
    # However, the state needs to track the last node to compute overlaps.
    # State: dp[mask][last_node] = max length? No, mask is too big (2^250).
    # But wait, we just need the longest path in a DAG.
    # In a general DAG, finding the longest path is O(V+E) using topological sort + DP.
    # Is the graph guaranteed to be a DAG? Yes, "no sequence ... ever forms a cycle".
    # So we can simply:
    # 1. Build the graph (adjacency list).
    # 2. Perform topological sort.
    # 3. Run DP to find the longest path ending at each node.
    # 4. Reconstruct the path.
    # 5. Check for ambiguity (multiple paths with same max length).

    # Step 1: Build Graph
    # Overlap condition: suffix of A (len >= 5) == prefix of B.
    # Since overlap is unique, we just find the longest valid overlap.
    
    graph = {i: [] for i in range(n)}
    in_degree = [0] * n
    
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            # Check if fragments[i] can precede fragments[j]
            # We need the longest overlap k such that 5 <= k <= min(len(i), len(j))
            # and fragments[i][-k:] == fragments[j][:k]
            
            best_k = 0
            max_possible = min(len(fragments[i]), len(fragments[j]))
            
            # Since n is small (250) and string length is small (80), we can brute force k.
            # Actually, we only care if there exists a k >= 5.
            # The problem says "whenever fragment A immediately precedes fragment B: A has a suffix ... equal to a prefix ... length at least 5".
            # It also says "two fragments that satisfy these criteria do so in exactly one way".
            # This implies if there are multiple k's >= 5, only one is valid? Or rather, the overlap is unique.
            # Usually in such problems, we take the longest possible overlap to maximize the resulting string length, 
            # but the problem statement says "optimal reconstruction ... maximizes the number of fragments".
            # The reconstruction rule uses the shared suffix/prefix. If there were multiple valid overlaps, 
            # the resulting string would differ. But the problem says "unique way", so we just find the one k >= 5.
            
            found = False
            for k in range(max_possible, 4, -1):
                if fragments[i].endswith(fragments[j][:k]):
                    best_k = k
                    found = True
                    break
            
            if found:
                graph[i].append(j)
                in_degree[j] += 1

    # Step 2: Topological Sort
    # Since it's a DAG, we can use Kahn's algorithm.
    queue = []
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    
    topo_order = []
    idx = 0
    while idx < len(queue):
        u = queue[idx]
        idx += 1
        topo_order.append(u)
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    
    # If topo_order length < n, there is a cycle. But problem guarantees no cycles.
    
    # Step 3: DP for Longest Path
    # dp[u] = (max_fragments_count, predecessor_node)
    # Initialize dp[u] = (1, -1) for all u
    dp_count = [1] * n
    dp_prev = [-1] * n
    
    # Process in topological order
    for u in topo_order:
        for v in graph[u]:
            # If we extend path from u to v
            if dp_count[u] + 1 > dp_count[v]:
                dp_count[v] = dp_count[u] + 1
                dp_prev[v] = u
            elif dp_count[u] + 1 == dp_count[v]:
                # Ambiguity check: multiple predecessors give same max length
                # We need to track if there are multiple ways to achieve the max length ending at v
                # But wait, the problem asks if the *reconstruction* is ambiguous.
                # If there are two different paths of the same maximal length, it's ambiguous.
                # We can detect this by checking if any node has >1 parent in the optimal subgraph.
                pass

    # Find the global maximum
    max_len = 0
    candidates = []
    for i in range(n):
        if dp_count[i] > max_len:
            max_len = dp_count[i]
            candidates = [i]
        elif dp_count[i] == max_len:
            candidates.append(i)
    
    if max_len == 0:
        # Should not happen as n >= 1
        print("AMBIGUOUS")
        return

    # Check for ambiguity
    # Ambiguity exists if there are multiple paths of length max_len.
    # This happens if:
    # 1. There are multiple end nodes with dp_count == max_len.
    # 2. OR, for some node v with dp_count == max_len, there are multiple predecessors u such that dp_count[u] + 1 == dp_count[v].
    
    is_ambiguous = False
    
    # Check multiple end nodes
    if len(candidates) > 1:
        is_ambiguous = True
    else:
        end_node = candidates[0]
        # Backtrack to check for multiple parents at any step
        curr = end_node
        path_nodes = [curr]
        while curr != -1:
            # Count how many parents u satisfy: u -> curr AND dp_count[u] + 1 == dp_count[curr]
            # Note: In a DAG, a node can have multiple incoming edges.
            # We need to check if there's more than one such u that lies on a longest path.
            # Since we processed in topo order, dp_count[curr] is final.
            # We can just look at all incoming edges to curr.
            count = 0
            best_parent = -1
            for u in range(n):
                if u in graph and curr in graph[u]: # u -> curr
                    if dp_count[u] + 1 == dp_count[curr]:
                        count += 1
                        best_parent = u
            if count > 1:
                is_ambiguous = True
                break
            curr = best_parent
            if curr == -1:
                break
    
    if is_ambiguous:
        print("AMBIGUOUS")
    else:
        # Reconstruct the path
        path = []
        curr = end_node
        while curr != -1:
            path.append(curr)
            curr = dp_prev[curr]
        path.reverse()
        
        # Build the string
        result = fragments[path[0]]
        for i in range(1, len(path)):
            prev_frag = fragments[path[i-1]]
            curr_frag = fragments[path[i]]
            # Find overlap
            # We know there is exactly one overlap >= 5
            # Find the longest one (or the one used in our graph construction)
            # Our graph construction used the longest k >= 5.
            # Let's re-verify the overlap length to be safe.
            max_possible = min(len(prev_frag), len(curr_frag))
            overlap_len = 0
            for k in range(max_possible, 4, -1):
                if prev_frag.endswith(curr_frag[:k]):
                    overlap_len = k
                    break
            
            # Append the non-overlapping part
            result += curr_frag[overlap_len:]
        
        print(result)

if __name__ == "__main__":
    solve()