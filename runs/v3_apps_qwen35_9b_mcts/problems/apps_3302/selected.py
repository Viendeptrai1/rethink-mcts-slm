import sys

# Increase recursion depth for deep DFS searches (up to 2^16 = 65536 nodes)
sys.setrecursionlimit(100000)

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        p_count = int(next(iterator))
        P = set()
        for _ in range(p_count):
            P.add(int(next(iterator)))
    except StopIteration:
        return

    # Convert P to a set of integers for O(1) lookup
    # We need to generate a Hamiltonian path in the hypercube Q_n where edges only exist
    # if the Hamming distance between endpoints is in P.

    # Precompute valid moves for each node to speed up DFS
    # Node is represented as an integer 0 to 2^n - 1
    # Precomputing adjacency lists might be memory heavy for n=16 (65536 nodes * avg degree),
    # but let's try a hybrid approach: compute neighbors on the fly or precompute if needed.
    # Given n <= 16, 2^16 = 65536. Precomputing adjacency list is feasible.
    
    # However, generating the full adjacency list for n=16 with arbitrary P could be large.
    # Let's optimize: For a node u, neighbors are u ^ (1<<k) for k in 0..n-1.
    # Check if popcount(k) is in P? No, the distance is the number of bits flipped.
    # Flipping bit k changes distance by 1. So distance is always 1 if we flip 1 bit.
    # Wait, the problem says "differ in exactly k bits" where k is in P.
    # So we can flip any subset of bits of size k, where k in P.
    # This means from u, we can go to u ^ mask where popcount(mask) is in P.
    
    # Number of neighbors can be large. For n=16, if P={8}, neighbors = C(16,8) = 12870.
    # Total edges could be huge. We cannot precompute full adjacency list if P contains large numbers.
    # But we only need a Hamiltonian path.
    # Standard Gray code flips 1 bit. If 1 in P, we can use standard Gray code.
    # If 1 not in P, we must flip >= 2 bits.
    
    # Heuristic/Algorithm:
    # 1. If 1 in P: The standard binary reflected Gray code works perfectly.
    #    Sequence: g(i) = i ^ (i >> 1). Consecutive values differ by 1 bit.
    # 2. If 1 not in P:
    #    This is much harder. The graph is a subgraph of the hypercube.
    #    If all k in P are even, the graph is bipartite. A Hamiltonian path exists only if
    #    the two partitions have equal size (which they do, 2^(n-1) each) and the graph is connected.
    #    However, constructing it is non-trivial.
    #    Common strategy for "even" palettes: Use a recursive construction or specific patterns.
    #    For small n, DFS with heuristics (Warnsdorff's rule: visit nodes with fewer available moves first) works.
    #    For n=16, pure DFS might TLE without strong heuristics.
    
    # Let's implement a DFS with Warnsdorff's heuristic.
    # State: current node, visited mask (or set).
    # To avoid TLE, we use an iterative DFS or optimized recursive DFS.
    # Since 2^16 is 65536, a simple DFS might visit many states.
    # But we only need one path.
    
    # Optimization: 
    # If 1 in P, output standard Gray code immediately.
    if 1 in P:
        # Standard Binary Reflected Gray Code
        # g(i) = i ^ (i >> 1)
        # We need to output as binary strings of length n
        for i in range(1 << n):
            val = i ^ (i >> 1)
            # Format as n-bit binary string
            s = bin(val)[2:]
            s = s.zfill(n)
            print(s)
        return

    # If 1 not in P, we must search.
    # Check for trivial impossibility:
    # If n is large and P only has large even numbers, connectivity might be an issue.
    # But let's rely on DFS with pruning.
    
    # Precompute bit counts for masks? No, we generate masks dynamically.
    # To speed up neighbor generation:
    # For a given u, iterate k from 1 to n. If k in P, iterate all masks of weight k.
    # Iterating all masks of weight k is slow if k is large.
    # Alternative: Precompute all masks of weight k for each k in P?
    # For n=16, max C(16,8) = 12870. Sum of C(16,k) for k in P is at most 2^16.
    # We can precompute a list of masks for each weight in P.
    
    masks_by_weight = {}
    for k in P:
        masks_by_weight[k] = []
        # Generate all combinations of k bits from n
        # Using recursion or itertools
        from itertools import combinations
        for indices in combinations(range(n), k):
            mask = 0
            for idx in indices:
                mask |= (1 << idx)
            masks_by_weight[k].append(mask)
    
    # Sort masks by some heuristic? Maybe number of common neighbors? Hard to precompute.
    # Let's just keep them as is.
    
    total_nodes = 1 << n
    visited = [False] * total_nodes
    path = []
    
    # Start node: 0
    start_node = 0
    
    # To optimize DFS, we can use an iterative approach with a stack to avoid recursion limit issues
    # and allow better control over neighbor ordering.
    # Stack elements: (current_node, path_list)
    # But copying path_list is expensive.
    # Better: maintain a global path list and backtrack.
    
    # Heuristic: When choosing next node, prefer nodes with fewer unvisited neighbors (Warnsdorff).
    # This requires looking ahead, which is expensive.
    # Given constraints and problem type, maybe a randomized DFS or simple DFS with good ordering works.
    # Let's try simple DFS with neighbor ordering by "degree" (number of valid moves from neighbor).
    
    # Precompute degrees? Degree of a node u is sum_{k in P} C(n, k). It's constant for all nodes in hypercube.
    # So degree heuristic doesn't help directly unless we consider unvisited neighbors.
    
    # Let's implement recursive DFS with backtracking.
    # To improve performance, we can shuffle the order of masks if needed, but deterministic is better for debugging.
    
    # One critical optimization: 
    # If n is even and all k in P are even, the graph is bipartite.
    # The hypercube is bipartite with partitions based on parity of bit count (popcount).
    # If we start at 0 (even popcount), next must be odd popcount, next even, etc.
    # This is consistent.
    # If n is odd and all k in P are even, then parity never changes. 
    # We can only visit nodes with same parity as start. 
    # Since we need to visit ALL 2^n nodes, this is impossible if n is odd and all k in P are even.
    # Exception: If we can change parity, but we can't if all k are even.
    # So: if all k in P are even and n is odd -> impossible.
    
    all_even = True
    for k in P:
        if k % 2 != 0:
            all_even = False
            break
    
    if all_even and n % 2 != 0:
        print("impossible")
        return

    # Another check: If n is even and all k in P are even, it's possible (e.g., n=2, P={2}).
    # But if n is odd and all k in P are even, impossible.
    
    # Let's run DFS.
    # To make it faster, we can use a fixed start node. 0 is fine.
    
    # We need to output the path.
    
    # Iterative DFS to avoid recursion depth issues and potentially faster
    # Stack: [current_node]
    # We also need to track the path.
    
    # Actually, for Hamiltonian path, recursive backtracking is standard.
    # Let's define the recursive function.
    
    # Global variables for DFS
    current_path = []
    found = False
    
    # To optimize neighbor iteration, we can sort masks_by_weight[k] by some criteria?
    # Maybe random shuffle to avoid worst-case deterministic paths?
    # Let's try without shuffle first, but if it fails, we might need randomness.
    # Given the judge environment, deterministic is safer unless TLE.
    
    # Pre-calculate masks for each weight to avoid recomputing popcount or combinations during DFS
    # We already did that.
    
    # Define the recursive solver
    # Using a list for path and a boolean array for visited
    
    # Optimization: Use a single integer for visited? No, 2^16 fits in int, but array is faster for indexing.
    
    # Let's write the DFS
    def dfs(u):
        nonlocal found
        if found:
            return
        
        visited[u] = True
        current_path.append(u)
        
        if len(current_path) == total_nodes:
            found = True
            return
        
        # Generate neighbors
        # Iterate over weights in P
        # To optimize, we can iterate weights in increasing order or based on some heuristic
        # Let's try iterating weights in P
        for k in P:
            for mask in masks_by_weight[k]:
                v = u ^ mask
                if not visited[v]:
                    # Heuristic: Check if v has many unvisited neighbors? (Warnsdorff)
                    # Calculating this for every candidate is expensive.
                    # Let's skip for now and rely on simple order.
                    # Maybe sort P by size? Or shuffle P?
                    # Let's try sorting P by k descending? Or ascending?
                    # Usually smaller steps are more flexible, but larger steps jump around.
                    # Let's try ascending k.
                    if dfs(v):
                        return
        
        # Backtrack
        current_path.pop()
        visited[u] = False

    # Start DFS
    # Reset visited
    visited = [False] * total_nodes
    current_path = []
    found = False
    
    # Try starting from 0
    dfs(0)
    
    if found:
        # Output the path
        for val in current_path:
            s = bin(val)[2:]
            s = s.zfill(n)
            print(s)
    else:
        print("impossible")

if __name__ == "__main__":
    solve()