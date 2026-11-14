import sys
from collections import deque

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = [0] + [int(x) for x in data[1:]]  # 1-based indexing
    
    # Determine parity of each element
    # 0 for even, 1 for odd
    parity = [0] * (n + 1)
    for i in range(1, n + 1):
        parity[i] = a[i] % 2
    
    # We need to find the shortest distance from each node to any node with opposite parity.
    # Instead of running BFS from each node, we reverse the graph and run multi-source BFS
    # starting from all nodes that have the target parity.
    
    # Build reversed adjacency list
    # If there is an edge i -> j in original graph, we add j -> i in reversed graph.
    # Original edges from i: i - a[i] and i + a[i]
    # So in reversed graph, from node u, we can go to v if v - a[v] == u or v + a[v] == u.
    # But it's easier to just store the forward edges and then reverse the logic during BFS?
    # Actually, standard trick: 
    # We want dist[i] = min distance from i to any node with opposite parity.
    # Let's define target nodes: all j such that parity[j] != parity[i].
    # Since the condition depends on i, we split into two cases:
    # Case 1: i is odd, we want to reach any even node.
    # Case 2: i is even, we want to reach any odd node.
    #
    # We can run two BFS traversals:
    # 1. Start BFS from all even nodes. Compute distances to all nodes. For odd nodes, this distance is the answer.
    # 2. Start BFS from all odd nodes. Compute distances to all nodes. For even nodes, this distance is the answer.
    #
    # However, the graph is directed. The edge is i -> i - a[i] and i -> i + a[i].
    # If we start BFS from target nodes (say all even nodes), we need to traverse backwards along the edges.
    # Backward edge: if original edge is u -> v, then backward is v -> u.
    # Original: from u, we can go to v = u - a[u] or v = u + a[u].
    # So in backward graph, from v, we can go to u if u - a[u] == v or u + a[u] == v.
    # This means for a given v, we need to find all u such that u - a[u] == v OR u + a[u] == v.
    # u - a[u] = v => u = v + a[u] (circular dependency)
    # u + a[u] = v => u = v - a[u] (circular dependency)
    #
    # Alternative approach:
    # Instead of building the reversed graph explicitly (which is hard because u depends on a[u]),
    # we can just build the forward graph and run BFS from sources? No, we need shortest path TO targets.
    #
    # Let's reconsider the reversed graph construction.
    # We want to find for each u, the shortest path to any v with opposite parity.
    # Let's create a reversed graph where edges go from v to u if there is an edge u->v in original.
    # Edge u->v exists if v = u - a[u] or v = u + a[u].
    # So in reversed graph, from v, we have edges to u if u - a[u] == v or u + a[u] == v.
    # This is equivalent to: u = v + a[u] (if v = u - a[u]) -> u - a[u] = v.
    # Or u = v - a[u] (if v = u + a[u]) -> u + a[u] = v.
    #
    # Notice that a[u] is fixed for each u.
    # So for a specific v, the possible predecessors u are those where:
    # 1. u - a[u] = v  => u = v + a[u]. This doesn't help directly to find u without knowing a[u].
    # 2. u + a[u] = v  => u = v - a[u].
    #
    # Wait, we can iterate over all u and add edges to the reversed graph explicitly.
    # There are N nodes. Each node u has at most 2 outgoing edges.
    # So we can build the reversed graph in O(N).
    # reversed_adj[v].append(u) if u -> v exists.
    
    reversed_adj = [[] for _ in range(n + 1)]
    
    for u in range(1, n + 1):
        val = a[u]
        # Edge u -> u - val
        v1 = u - val
        if 1 <= v1 <= n:
            reversed_adj[v1].append(u)
        
        # Edge u -> u + val
        v2 = u + val
        if 1 <= v2 <= n:
            reversed_adj[v2].append(u)
            
    # Now run BFS
    # Initialize answer array with -1
    ans = [-1] * (n + 1)
    
    # BFS 1: Start from all even nodes, compute distances. These distances are valid for odd nodes.
    # Queue contains (node, distance)
    q = deque()
    dist_even = [-1] * (n + 1)
    
    for i in range(1, n + 1):
        if parity[i] == 0: # even
            dist_even[i] = 0
            q.append(i)
            
    while q:
        u = q.popleft()
        d = dist_even[u]
        
        for v in reversed_adj[u]:
            if dist_even[v] == -1:
                dist_even[v] = d + 1
                q.append(v)
    
    # For all odd nodes, the answer is dist_even[node]
    for i in range(1, n + 1):
        if parity[i] == 1:
            ans[i] = dist_even[i]
            
    # BFS 2: Start from all odd nodes, compute distances. These distances are valid for even nodes.
    q = deque()
    dist_odd = [-1] * (n + 1)
    
    for i in range(1, n + 1):
        if parity[i] == 1: # odd
            dist_odd[i] = 0
            q.append(i)
            
    while q:
        u = q.popleft()
        d = dist_odd[u]
        
        for v in reversed_adj[u]:
            if dist_odd[v] == -1:
                dist_odd[v] = d + 1
                q.append(v)
                
    # For all even nodes, the answer is dist_odd[node]
    for i in range(1, n + 1):
        if parity[i] == 0:
            ans[i] = dist_odd[i]
            
    # Output results for 1 to n
    print(*(ans[1:]))

if __name__ == '__main__':
    solve()