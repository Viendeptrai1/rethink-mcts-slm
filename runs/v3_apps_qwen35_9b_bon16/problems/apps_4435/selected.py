import sys
from collections import deque

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    n = int(next(iterator))
    a = [0] * (n + 1)
    for i in range(1, n + 1):
        a[i] = int(next(iterator))

    # Determine target parity for each position
    # We need to find distance to nearest node with opposite parity
    # We can run BFS from all target nodes simultaneously
    
    # Identify starting points for BFS based on parity
    # If a[i] is odd, we want to reach even positions
    # If a[i] is even, we want to reach odd positions
    
    # Build adjacency: from i, can go to i - a[i] and i + a[i] if within bounds
    # Since edges are directed, we build the graph as is
    
    # We will run two BFS traversals:
    # 1. From all odd positions, find distances to nearest even position
    # 2. From all even positions, find distances to nearest odd position
    # Then assign d[i] accordingly
    
    # Initialize distance arrays
    dist_odd_to_even = [-1] * (n + 1)
    dist_even_to_odd = [-1] * (n + 1)
    
    # BFS queue for odd -> even
    q_odd = deque()
    # BFS queue for even -> odd
    q_even = deque()
    
    # Initialize queues and distances
    for i in range(1, n + 1):
        if a[i] % 2 == 1:
            # This is an odd node, target is even
            # We will compute dist_odd_to_even[i] later
            pass
        else:
            # This is an even node, target is odd
            # We will compute dist_even_to_odd[i] later
            pass
            
    # Actually, let's reverse the logic for BFS:
    # To find shortest path from ANY odd node to ANY even node efficiently:
    # We can start BFS from ALL even nodes (as targets) but since edges are directed i->j,
    # we need to reverse the graph to run BFS from targets? 
    # No, the problem asks: for each i, min moves to reach j with opposite parity.
    # This is a standard multi-source BFS if we fix the source set and target set.
    # But the graph is directed. 
    # 
    # Correct approach:
    # Case 1: For all odd i, we want min distance to any even j.
    #   We can run BFS starting from ALL even nodes in the REVERSED graph.
    #   In reversed graph, edge j->i exists if in original graph i->j.
    #   Then distance from even node j to odd node i in reversed graph = distance from i to j in original.
    #   So we initialize queue with all even nodes (in reversed graph sense, meaning they are sources for reversed BFS)
    #   and set their distance to 0. Then propagate.
    #
    # However, constructing the reversed graph explicitly takes O(N) which is fine.
    # Let's build the reversed graph.
    
    # Reversed graph: rev_adj[j] contains list of i such that i -> j in original graph
    # Original: i can go to i - a[i] and i + a[i]
    # So rev_adj[i - a[i]].append(i) and rev_adj[i + a[i]].append(i)
    
    rev_adj = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        val = a[i]
        left = i - val
        right = i + val
        if 1 <= left <= n:
            rev_adj[left].append(i)
        if 1 <= right <= n:
            rev_adj[right].append(i)
            
    # BFS 1: Find for each odd i, min dist to any even j
    # In reversed graph, start BFS from all even nodes.
    # dist1[i] = min steps from i (in original) to any even node
    # In reversed graph, this is dist from even nodes to i.
    
    dist1 = [-1] * (n + 1)
    q1 = deque()
    
    # Initialize with all even nodes
    for i in range(1, n + 1):
        if a[i] % 2 == 0:
            dist1[i] = 0
            q1.append(i)
            
    while q1:
        u = q1.popleft()
        d = dist1[u]
        for v in rev_adj[u]:
            if dist1[v] == -1:
                dist1[v] = d + 1
                q1.append(v)
                
    # BFS 2: Find for each even i, min dist to any odd j
    # In reversed graph, start BFS from all odd nodes.
    dist2 = [-1] * (n + 1)
    q2 = deque()
    
    # Initialize with all odd nodes
    for i in range(1, n + 1):
        if a[i] % 2 == 1:
            dist2[i] = 0
            q2.append(i)
            
    while q2:
        u = q2.popleft()
        d = dist2[u]
        for v in rev_adj[u]:
            if dist2[v] == -1:
                dist2[v] = d + 1
                q2.append(v)
                
    # Construct result
    res = []
    for i in range(1, n + 1):
        if a[i] % 2 == 1:
            # i is odd, need even target -> use dist1
            res.append(dist1[i])
        else:
            # i is even, need odd target -> use dist2
            res.append(dist2[i])
            
    print(*(res))

if __name__ == '__main__':
    solve()