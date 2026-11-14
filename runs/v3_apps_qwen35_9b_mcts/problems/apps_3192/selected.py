import sys
from collections import deque

def solve():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        n_line = next(iterator).strip()
        while not n_line:
            n_line = next(iterator).strip()
        n = int(n_line)
        
        names_line = next(iterator).strip()
        files = names_line.split()
        
        adj = {f: [] for f in files}
        
        for _ in range(n):
            header = next(iterator).strip()
            parts = header.split()
            filename = parts[0]
            k = int(parts[1])
            
            for _ in range(k):
                imp_line = next(iterator).strip()
                # Format: "import file1, file2, ..."
                if imp_line.startswith("import "):
                    deps_str = imp_line[7:]
                    deps = [d.strip() for d in deps_str.split(",")]
                    for d in deps:
                        if d in adj:
                            adj[filename].append(d)
                            
    except StopIteration:
        return

    # Check for self-loops first (cycle of length 1)
    for f in files:
        if f in adj[f]:
            print(f)
            return

    # BFS from each node to find the shortest cycle containing that node
    min_cycle_len = float('inf')
    best_cycle = None

    for start in files:
        # BFS state: (current_node, distance_from_start, parent_node)
        # We want to find a path from start to start (cycle)
        # Since we are looking for the shortest cycle, we can run BFS from 'start'
        # and look for the first time we see 'start' again via a non-parent edge.
        
        # However, standard BFS from a single source finds shortest paths to all nodes.
        # To find the shortest cycle involving 'start', we can run BFS starting at 'start'.
        # When we encounter 'start' again, the distance + 1 is the cycle length.
        # But we must ensure we don't just go back to the immediate parent.
        
        # Actually, a more robust way for unweighted graphs to find the shortest cycle 
        # is to run BFS from every node, but that's O(V*(V+E)). With V=500, V^2 = 250,000, which is fine.
        # But we can optimize: run BFS from each node u, treating u as the root.
        # We look for the first neighbor v of u such that v is already visited in the BFS tree 
        # and v is not the parent of u in the BFS tree? No, that's for general cycles.
        # For a cycle containing u, we want the shortest path from u to u.
        # This is equivalent to finding the shortest path between any two neighbors of u in the graph,
        # plus 2 (u -> neighbor1 ... neighbor2 -> u).
        # OR simply: Run BFS from u. If we hit u again, we found a cycle.
        # But BFS from u will naturally visit u at distance 0. We need to detect when we return to u.
        
        # Correct approach for shortest cycle containing 'start':
        # Run BFS starting at 'start'. Maintain distances.
        # When exploring neighbors of a node 'curr', if we see 'start', we found a cycle of length dist[curr] + 1.
        # Since BFS guarantees shortest paths, the first time we see 'start' (other than the start node itself)
        # gives the shortest cycle length for that start node.
        
        # Wait, if we start BFS at 'start', the queue initially has ('start', 0).
        # We mark 'start' as visited.
        # When we pop 'curr', we look at neighbors. If a neighbor is 'start', cycle found.
        # Is it possible that the shortest cycle doesn't involve 'start' as the "root" of the BFS?
        # Yes, but we are iterating 'start' over all nodes. So eventually we will pick a node on the shortest cycle
        # and find it. The shortest cycle in the graph will be found when we start BFS from one of its nodes.
        # And since BFS expands layer by layer, the first time we close a loop back to the start node,
        # it is the shortest cycle passing through that start node.
        
        # One caveat: If the graph is undirected, we might find the same cycle twice. That's fine.
        # If the graph is directed (which it is), this logic holds.
        
        # Let's refine the BFS for a specific 'start':
        # dist = {start: 0}
        # parent = {start: None}
        # queue = deque([start])
        # while queue:
        #   curr = queue.popleft()
        #   for nxt in adj[curr]:
        #     if nxt == start:
        #       cycle_len = dist[curr] + 1
        #       # Reconstruct path
        #       path = [curr]
        #       temp = start # This is the target to close the loop
        #       # We need the path from start to curr, then append start?
        #       # No, the cycle is start -> ... -> curr -> start.
        #       # We need the path from start to curr.
        #       # But our parent map tracks path from start.
        #       # So we can reconstruct path from curr back to start.
        #       # Then reverse it to get start -> ... -> curr.
        #       # Then the cycle is that path + [start].
        #       # But wait, the output format requires the cycle to start with the file name?
        #       # "output a line containing the names of files in a shortest cycle"
        #       # "ith file listed must import the (i+1)st file"
        #       # So if cycle is A->B->C->A, output could be A B C.
        #       # A imports B, B imports C, C imports A.
        #       # Our path reconstruction: start -> ... -> curr.
        #       # Then curr imports start.
        #       # So the sequence is start, ..., curr.
        #       # Let's verify: start imports next, ..., curr imports start.
        #       # Yes.
        #       pass
        #     elif nxt not in dist:
        #       dist[nxt] = dist[curr] + 1
        #       parent[nxt] = curr
        #       queue.append(nxt)
        
        # However, there is a catch. If we start BFS at 'start', and there is a cycle not involving 'start',
        # we won't find it. But we iterate all 'start', so we will find the global shortest cycle.
        # The issue is efficiency. O(V * (V+E)). V=500, E <= V*V. 500 * 250000 = 125,000,000 operations.
        # In Python, this might be tight for 1-2 seconds.
        # Can we optimize?
        # We only need to run BFS from nodes that are part of a cycle? We don't know them.
        # But note: if we find a cycle of length L, we can stop if L=3 (minimum possible for simple cycle in directed graph without self loops).
        # But we might find a longer one first.
        # Actually, we can stop as soon as we find ANY cycle? No, we need the SHORTEST.
        # But if we process nodes in an order? No.
        # However, 125M simple operations (dict lookups, appends) might pass in PyPy, but in CPython it's risky.
        # Let's try to optimize the BFS.
        # We can use an array for visited/distance instead of a dict for speed.
        # Map file names to indices 0..n-1.
        
        pass

    # Re-implementing with indices for performance
    file_to_idx = {f: i for i, f in enumerate(files)}
    adj_idx = [[] for _ in range(n)]
    for f in files:
        for neighbor in adj[f]:
            adj_idx[file_to_idx[f]].append(file_to_idx[neighbor])

    min_len = float('inf')
    best_path = None

    # Pre-allocate arrays to avoid reallocation in loop
    dist = [0] * n
    parent = [-1] * n
    queue = deque()
    
    # We need a way to reset visited efficiently. 
    # Using a 'visited_token' array is faster than clearing a list.
    visited_token = [0] * n
    current_token = 0

    for start_node in range(n):
        # If we already found a cycle of length 3, we can't do better.
        if min_len == 3:
            break
            
        current_token += 1
        queue.clear()
        
        # Initialize BFS for start_node
        dist[start_node] = 0
        parent[start_node] = -1
        visited_token[start_node] = current_token
        queue.append(start_node)
        
        found = False
        
        while queue:
            u = queue.popleft()
            d_u = dist[u]
            
            # If the distance from start is already >= min_len, we can't find a shorter cycle through this path
            # because the cycle length would be at least d_u + 1 (if we close to start)
            # Actually, if d_u >= min_len, then any cycle closing at u would be > min_len.
            # But we might close the cycle at a neighbor.
            # Cycle length = d_u + 1. If d_u + 1 >= min_len, we can prune?
            # Yes, if d_u + 1 >= min_len, we don't care about cycles found from here.
            if d_u + 1 >= min_len:
                continue

            for v in adj_idx[u]:
                if v == start_node:
                    # Found a cycle
                    cycle_len = d_u + 1
                    if cycle_len < min_len:
                        min_len = cycle_len
                        # Reconstruct path
                        path = []
                        curr = u
                        while curr != -1:
                            path.append(files[curr])
                            curr = parent[curr]
                        path.reverse()
                        # The cycle is path + [start_node] but the last element of path imports start_node.
                        # The sequence is: path[0] -> path[1] -> ... -> path[-1] -> path[0]
                        # So the list of files is path.
                        best_path = path
                    found = True
                    # Since BFS guarantees shortest path to u, the first time we see start_node
                    # is the shortest cycle for this start_node.
                    # But we might find a shorter cycle from another start_node later?
                    # We continue to check other start_nodes to ensure global minimum.
                    # However, if we found a cycle of length L, we can prune any search where d_u + 1 >= L.
                    # We already added that check.
                    break 
                
                if visited_token[v] != current_token:
                    visited_token[v] = current_token
                    dist[v] = d_u + 1
                    parent[v] = u
                    queue.append(v)
        
        if found:
            # Optimization: if we found a cycle, we can potentially stop early if min_len is 3?
            # Yes, handled by the check at the start of the loop.
            pass

    if best_path:
        print(" ".join(best_path))
    else:
        print("SHIP IT")

if __name__ == "__main__":
    solve()