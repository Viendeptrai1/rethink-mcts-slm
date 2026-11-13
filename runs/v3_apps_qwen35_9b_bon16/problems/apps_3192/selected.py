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
        file_to_idx = {name: i for i, name in enumerate(files)}
        
        adj = [[] for _ in range(n)]
        
        for _ in range(n):
            line = next(iterator).strip()
            parts = line.split()
            filename = parts[0]
            k = int(parts[1])
            
            # Next k lines are imports
            for _ in range(k):
                imp_line = next(iterator).strip()
                # Format: "import file1, file2, ..."
                if imp_line.startswith("import "):
                    deps_str = imp_line[7:]
                    deps = [d.strip() for d in deps_str.split(",")]
                    for dep in deps:
                        if dep in file_to_idx:
                            adj[file_to_idx[filename]].append(file_to_idx[dep])
        
        # Find shortest cycle using BFS from each node
        # Since n <= 500, O(n*(n+m)) is acceptable.
        
        min_cycle_len = float('inf')
        best_cycle = None
        
        for start_node in range(n):
            # BFS to find shortest path back to start_node
            # We need to track distance and parent to reconstruct cycle
            # However, standard BFS finds shortest path between two nodes.
            # To find shortest cycle involving start_node:
            # Run BFS from start_node. If we encounter start_node again, that's a cycle.
            # But wait, BFS tree edges don't form cycles except the one we close.
            # Actually, the shortest cycle containing 'start_node' is found by running BFS 
            # from 'start_node' and looking for the first time we see 'start_node' again?
            # No, that's not right because BFS explores layer by layer.
            # Correct approach for unweighted graph shortest cycle:
            # For each node u, run BFS. Maintain dist[u] = 0.
            # When exploring edge (u, v):
            #   If v is unvisited: dist[v] = dist[u] + 1, parent[v] = u
            #   If v is visited and v != parent[u]: cycle found of length dist[u] + dist[v] + 1?
            #   No, that's for finding any cycle. For shortest cycle specifically:
            #   We can run BFS from every node. The first time we meet a visited node that is 
            #   part of the current BFS tree but not the immediate parent, we found a cycle.
            #   Length = dist[u] + dist[v] + 1.
            #   But we must ensure the cycle includes the start_node? 
            #   Actually, if we run BFS from start_node, the first cycle we find (back edge) 
            #   will be the shortest cycle passing through start_node? Not necessarily.
            #   
            # Better approach: 
            # The shortest cycle in the entire graph is min over all nodes u of the shortest 
            # cycle containing u.
            # To find shortest cycle containing u:
            # Run BFS from u. Keep track of distances. 
            # When we see an edge (x, y) where y is already visited:
            #   If y is u, we found a cycle of length dist[x] + 1.
            #   If y is not u, and y is in the current BFS tree, then we have a cycle. 
            #   The length is dist[x] + dist[y] + 1. But this cycle might not pass through u?
            #   Actually, if we start BFS from u, any back edge (x, y) where y is visited creates 
            #   a cycle. If y is an ancestor of x, the cycle is dist[x] - dist[y] + 1.
            #   This cycle passes through u ONLY IF y is an ancestor of x in the BFS tree rooted at u.
            #   But BFS tree is not necessarily a simple path.
            #   
            # Simpler approach given constraints (N=500):
            # Run BFS from EACH node s.
            # In the BFS, maintain dist array initialized to -1.
            # dist[s] = 0.
            # Queue q = [s].
            # While q:
            #   u = q.popleft()
            #   for v in adj[u]:
            #     if v == s:
            #       cycle_len = dist[u] + 1
            #       if cycle_len < min_cycle_len:
            #         min_cycle_len = cycle_len
            #         # Reconstruct path from s to u using parent pointers
            #         path = []
            #         curr = u
            #         while curr != s:
            #           path.append(curr)
            #           curr = parent[curr]
            #         path.append(s)
            #         path.reverse()
            #         best_cycle = path
            #         break
            #     elif dist[v] == -1:
            #       dist[v] = dist[u] + 1
            #       parent[v] = u
            #       q.append(v)
            #   if best_cycle is not None:
            #     break
            #
            # Does this guarantee the shortest cycle?
            # Yes, because BFS guarantees shortest paths from s. The first time we hit s again,
            # it is via the shortest path from s to some u plus edge (u,s).
            # So length = dist[u] + 1. Since we explore in increasing order of dist, the first
            # time we find such an edge, it is minimal for s.
            # And since we try all s, we find the global minimum.
            #
            # One caveat: What if the cycle does not include s? 
            # Then this BFS won't find it. But we iterate s over all nodes. Eventually s will be part of the cycle.
            # So yes, this works.
            
            best_cycle = None
            
            dist = [-1] * n
            parent = [-1] * n
            dist[start_node] = 0
            queue = deque([start_node])
            
            found = False
            while queue and not found:
                u = queue.popleft()
                for v in adj[u]:
                    if v == start_node:
                        # Found cycle
                        cycle_len = dist[u] + 1
                        if cycle_len < min_cycle_len:
                            min_cycle_len = cycle_len
                            # Reconstruct
                            path = []
                            curr = u
                            while curr != start_node:
                                path.append(files[curr])
                                curr = parent[curr]
                            path.append(files[start_node])
                            best_cycle = path
                            found = True
                        break
                    elif dist[v] == -1:
                        dist[v] = dist[u] + 1
                        parent[v] = u
                        queue.append(v)
            
            if found:
                break
        
        if best_cycle:
            print(" ".join(best_cycle))
        else:
            print("SHIP IT")
            
    except StopIteration:
        pass

if __name__ == "__main__":
    solve()