import sys

# Increase recursion depth just in case, though we will use iterative DFS/BFS
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        m = int(next(iterator))
    except StopIteration:
        return

    edges = []
    adj = [[] for _ in range(n + 1)]
    
    # Store edges to output later
    for i in range(m):
        u = int(next(iterator))
        v = int(next(iterator))
        edges.append((u, v))
        adj[u].append(v)
        adj[v].append(u)

    # The problem requires that the directed graph has no paths of length >= 2.
    # This means there are no sequences of vertices a -> b -> c.
    # In other words, every vertex can have at most one outgoing edge and at most one incoming edge?
    # No, that would be a matching.
    # Let's re-evaluate: "no paths of length two or greater".
    # A path of length 2 is u -> v -> w.
    # To prevent this, for any vertex v, it cannot be the case that (v has an incoming edge AND v has an outgoing edge).
    # So, for every vertex v, either:
    #   1. All edges incident to v are outgoing (v is a source for all its neighbors).
    #   2. All edges incident to v are incoming (v is a sink for all its neighbors).
    #
    # If a vertex has degree > 0, it must be either a pure source or a pure sink.
    # If a vertex is a pure source, all its incident edges are directed away from it.
    # If a vertex is a pure sink, all its incident edges are directed towards it.
    #
    # Consider the connected components. The graph is connected.
    # If we pick a root r and direct all edges away from r (BFS/DFS tree style), then:
    #   - r is a source (all outgoing).
    #   - Any other node v (v != r) has exactly one incoming edge from its parent in the BFS tree.
    #   - Does v have outgoing edges? Yes, to its children.
    #   - So if v has children, we have parent -> v -> child, which is a path of length 2.
    #
    # Therefore, a standard BFS/DFS orientation doesn't work if the tree has depth >= 2.
    #
    # Let's reconsider the condition: No path of length >= 2.
    # This implies the diameter of the directed graph is at most 1.
    # This means the underlying undirected graph must be a star graph?
    # Let's check.
    # If the graph is a star graph with center c and leaves l1, l2, ...
    # We can direct all edges as l1 -> c, l2 -> c, ... (all incoming to c).
    # Then there are no paths of length 2 because c has no outgoing edges.
    # Or we can direct all as c -> l1, c -> l2, ... (all outgoing from c).
    # Then there are no paths of length 2 because leaves have no outgoing edges.
    #
    # What if the graph is not a star?
    # Suppose we have a path 1-2-3.
    # Orientations:
    # 1->2, 2->3 => path 1->2->3 (length 2) - Bad.
    # 1->2, 3->2 => 1->2, 3->2. No path of length 2? 
    #    Path 1->2 is length 1. Path 3->2 is length 1. No path of length 2. OK.
    #    But wait, is 2 a source or sink? 
    #    2 has incoming from 1 and 3. So 2 is a sink.
    #    1 is a source. 3 is a source.
    #    This works for 1-2-3.
    #
    # What about 1-2-3-4?
    # If 2 is a sink, then 1->2 and 3->2.
    # Now consider 3. 3 has an edge to 2 (outgoing). Can 3 have an incoming edge from 4?
    # If 4->3, then we have 4->3->2 (path of length 2). Bad.
    # If 3->4, then we have 3->2 and 3->4. 3 is a source.
    # But 3 also has an edge to 2. So 3 is a source.
    # Now check 2. 2 has incoming from 1 and 3. So 2 is a sink.
    # Check 4. 4 has incoming from 3. So 4 is a sink.
    # Check 1. 1 has outgoing to 2. So 1 is a source.
    # Paths:
    # 1->2 (len 1)
    # 3->2 (len 1)
    # 3->4 (len 1)
    # Any path of length 2?
    # From 1: only to 2. 2 has no outgoing. OK.
    # From 3: to 2 and 4. 2 has no outgoing. 4 has no outgoing. OK.
    # So 1-2-3-4 works with orientation: 1->2, 3->2, 3->4.
    # Structure: 1->2, 3 is connected to 2 and 4.
    # Edges: (1,2), (2,3), (3,4).
    # Orientation: (1,2) is 1->2. (2,3) is 3->2. (3,4) is 3->4.
    # Vertices:
    # 1: out-degree 1, in-degree 0. (Source)
    # 2: in-degree 2, out-degree 0. (Sink)
    # 3: out-degree 2, in-degree 0. (Source)
    # 4: in-degree 1, out-degree 0. (Sink)
    # This works.
    #
    # General condition:
    # Every vertex must be either a pure source (all incident edges outgoing) or a pure sink (all incident edges incoming).
    # Let S be the set of sources, T be the set of sinks.
    # For any edge (u, v):
    #   If u in S and v in S: Impossible, because u would need to direct to v, but v is a source so it must direct away from its neighbors. Contradiction.
    #   If u in T and v in T: Impossible, because v would need to direct to u, but u is a sink.
    #   If u in S and v in T: u->v. Valid.
    #   If u in T and v in S: v->u. Valid.
    #
    # So the graph must be bipartite with partitions S and T.
    # And ALL edges must go from S to T.
    # This means the graph must be bipartite.
    # If the graph is bipartite, we can color it with 2 colors (0 and 1).
    # Let color 0 be set S (sources) and color 1 be set T (sinks).
    # Then for every edge (u, v), if u is color 0 and v is color 1, we direct u->v ('0').
    # If u is color 1 and v is color 0, we direct v->u ('1' relative to input order u,v? Wait).
    #
    # Let's formalize the output requirement.
    # Input edge i: u_i, v_i.
    # We need to output '0' if u_i -> v_i, '1' if v_i -> u_i.
    #
    # Strategy:
    # 1. Check if the graph is bipartite. If not, output "NO".
    # 2. If bipartite, perform 2-coloring. Let color[u] be 0 or 1.
    # 3. Define S = {u | color[u] == 0}, T = {u | color[u] == 1}.
    # 4. For each edge (u, v):
    #    If color[u] == 0 and color[v] == 1: direct u -> v. Output '0'.
    #    If color[u] == 1 and color[v] == 0: direct v -> u. Output '1'.
    #    (Since it's bipartite, these are the only cases).
    #
    # Does this satisfy the condition?
    # - Any path of length 2 would be a -> b -> c.
    # - a -> b implies color[a]=0, color[b]=1.
    # - b -> c implies color[b]=0, color[c]=1.
    # - But color[b] cannot be both 0 and 1. Contradiction.
    # - So no path of length 2 exists.
    #
    # What if the graph is not connected? The problem says "connected".
    # So we just need to check bipartiteness.
    #
    # Wait, is it possible that a non-bipartite graph can be oriented this way?
    # If the graph has an odd cycle, it's not bipartite.
    # In an odd cycle, you cannot 2-color it.
    # Can we orient an odd cycle without paths of length 2?
    # Cycle 1-2-3-1.
    # Try to assign Source/Sink.
    # If 1 is Source, 2 must be Sink (edge 1-2).
    # If 2 is Sink, 3 must be Source (edge 2-3).
    # If 3 is Source, 1 must be Sink (edge 3-1).
    # But 1 is Source. Contradiction.
    # So odd cycles are impossible.
    # Thus, the graph MUST be bipartite.
    
    # Algorithm:
    # 1. Build adjacency list.
    # 2. BFS/DFS to 2-color the graph.
    # 3. If conflict found (neighbor has same color), print NO.
    # 4. Else, iterate edges and print YES and the orientation string.

    color = [-1] * (n + 1)
    possible = True
    
    # Since graph is connected, one BFS from node 1 is enough.
    # But let's be safe and loop just in case (though problem guarantees connected).
    # Actually, problem says connected.
    
    queue = [1]
    color[1] = 0
    
    idx = 0
    while idx < len(queue):
        u = queue[idx]
        idx += 1
        c_u = color[u]
        
        for v in adj[u]:
            if color[v] == -1:
                color[v] = 1 - c_u
                queue.append(v)
            elif color[v] == c_u:
                possible = False
                break
        if not possible:
            break
    
    if not possible:
        print("NO")
    else:
        print("YES")
        res = []
        for u, v in edges:
            if color[u] == 0 and color[v] == 1:
                # u -> v
                res.append('0')
            else:
                # color[u] == 1 and color[v] == 0
                # v -> u
                res.append('1')
        print("".join(res))

if __name__ == '__main__':
    solve()