import sys
from collections import deque

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        p_count = int(next(iterator))
        palette = set()
        for _ in range(p_count):
            palette.add(int(next(iterator)))
    except StopIteration:
        return

    # If 1 is in the palette, we can use the standard reflected Gray code construction
    # because it only uses Hamming distance 1.
    if 1 in palette:
        result = []
        for i in range(1 << n):
            # Standard binary reflected Gray code: i ^ (i >> 1)
            g = i ^ (i >> 1)
            # Convert to binary string with leading zeros
            s = bin(g)[2:].zfill(n)
            result.append(s)
        print('\n'.join(result))
        return

    # If 1 is not in the palette, we must use a different approach.
    # The problem can be modeled as finding a Hamiltonian path in a hypercube where
    # edges are only allowed if the Hamming distance is in the palette.
    # Since n <= 16, the state space is up to 2^16 = 65536, which is manageable for BFS/DFS
    # if the graph is connected and has a Hamiltonian path. However, Hamiltonian path is NP-hard generally.
    # But for hypercubes with specific constraints, heuristics often work.
    #
    # Observation: If the palette does not contain 1, the graph is sparse or disconnected in many cases.
    # For example, if P = {n}, we can only move from x to ~x. This creates pairs of isolated edges (unless n=1).
    # If n=1 and P={1}, it works. If n>1 and P={n}, it's impossible because we get stuck after 2 nodes.
    #
    # General strategy:
    # 1. Check for obvious impossibility conditions.
    # 2. Use a heuristic search (like Warnsdorff's rule for knight's tour or simple degree-based DFS)
    #    to find a Hamiltonian path.
    #
    # Let's implement a DFS with backtracking and heuristics.
    # To optimize, we can precompute valid neighbors for each node.

    # Precompute neighbors
    # Node is represented as an integer from 0 to 2^n - 1
    total_nodes = 1 << n
    neighbors = [[] for _ in range(total_nodes)]
    
    # Generate all neighbors for each node based on palette
    # This might be O(2^n * n) which is fine for n=16 (16 * 65536 approx 1M)
    for mask in range(total_nodes):
        for k in palette:
            # Flip k-th bit (0-indexed)
            # The problem uses 1-based indexing for bit positions in description, 
            # but bit manipulation is 0-indexed. 
            # "s_i" is the bit position to flip. Let's assume 1 means least significant bit.
            # The example n=3, P={1} gives standard Gray code which flips LSB.
            neighbor = mask ^ (1 << (k - 1))
            neighbors[mask].append(neighbor)

    # Check connectivity and degrees
    # If any node has degree 0, impossible (unless total_nodes=1)
    if total_nodes > 1:
        for i in range(total_nodes):
            if len(neighbors[i]) == 0:
                print("impossible")
                return
    
    # Special case: n=1
    if n == 1:
        # Only two nodes: 0 and 1. Distance is 1.
        if 1 in palette:
            print("0")
            print("1")
        else:
            print("impossible")
        return

    # Heuristic DFS
    # We need to find a path of length 2^n visiting every node exactly once.
    # Start from node 0.
    
    path = []
    visited = [False] * total_nodes
    
    # Sort neighbors by degree (heuristic: visit nodes with fewer options first)
    # Recompute degrees dynamically or precompute? Precompute static degrees.
    degrees = [len(neighbors[i]) for i in range(total_nodes)]
    
    # We will modify the order of neighbors in the list 'neighbors' during the search?
    # No, let's just sort them once at the beginning based on static degrees.
    # But degrees change as we visit nodes (effectively removing them from available set).
    # A common heuristic is to sort neighbors by their current available degree.
    
    # Let's implement a recursive DFS with iterative deepening or just deep recursion with pruning.
    # Given 2^16, recursion depth is 65536. Python default limit is 1000.
    # We need to increase recursion limit or use iterative approach.
    # Iterative DFS with explicit stack is safer.
    
    # State for iterative DFS: (current_node, visited_mask) -> too big for mask
    # Instead, we maintain a path list and backtrack.
    # Since we need to visit all, and n is small, maybe simple DFS with good neighbor ordering works.
    
    # Increase recursion limit
    sys.setrecursionlimit(70000)
    
    # Pre-sort neighbors for each node by static degree (ascending)
    for i in range(total_nodes):
        neighbors[i].sort(key=lambda x: degrees[x])

    # DFS function
    def dfs(u, count):
        if count == total_nodes:
            return True
        
        visited[u] = True
        path.append(u)
        
        for v in neighbors[u]:
            if not visited[v]:
                if dfs(v, count + 1):
                    return True
        
        # Backtrack
        path.pop()
        visited[u] = False
        return False

    # Start DFS from 0
    if dfs(0, 1):
        # Construct output
        output_lines = []
        for u in path:
            output_lines.append(bin(u)[2:].zfill(n))
        print('\n'.join(output_lines))
    else:
        print("impossible")

solve()