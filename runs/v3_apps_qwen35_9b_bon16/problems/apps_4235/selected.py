import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    iterator = iter(data)
    n = int(next(iterator))
    m = int(next(iterator))
    
    edges = []
    for _ in range(m):
        u = int(next(iterator))
        v = int(next(iterator))
        edges.append((u, v))
    
    # Check if the graph is bipartite
    # We can use BFS/DFS to check bipartiteness and simultaneously assign colors (partitions)
    color = [-1] * (n + 1)
    is_bipartite = True
    
    # Since the graph is connected, we only need one BFS starting from vertex 1
    queue = [1]
    color[1] = 0
    
    idx = 0
    while idx < len(queue):
        u = queue[idx]
        idx += 1
        
        for v, _ in edges:
            if v == u:
                continue
            # Find the index of edge (u, v) or (v, u) in the edges list to identify it later if needed,
            # but for bipartite check we just need neighbors.
            # However, we need to traverse all edges. Let's build adjacency list.
            pass
    
    # Re-build adjacency list for traversal
    adj = [[] for _ in range(n + 1)]
    for i in range(m):
        u, v = edges[i]
        adj[u].append(v)
        adj[v].append(u)
    
    # BFS for bipartite check
    queue = [1]
    color[1] = 0
    idx = 0
    while idx < len(queue):
        u = queue[idx]
        idx += 1
        c = color[u]
        next_c = 1 - c
        
        for v in adj[u]:
            if color[v] == -1:
                color[v] = next_c
                queue.append(v)
            elif color[v] == c:
                is_bipartite = False
                break
        if not is_bipartite:
            break
            
    if not is_bipartite:
        print("NO")
        return
    
    # If bipartite, we can orient edges from partition 0 to partition 1.
    # This ensures no path of length >= 2 because:
    # - All edges go 0 -> 1.
    # - There are no edges within 0 or within 1.
    # - A path of length 2 would be 0->1->?, but there are no edges starting from 1 to anywhere (all edges from 1 would be to 0, which is against our orientation, or we just don't have edges 1->0).
    # Actually, if we orient all edges 0 -> 1:
    # Path: u -> v -> w. 
    # If u is in 0, v must be in 1 (edge u->v).
    # From v (in 1), can we go to w? Edges from v can only go to 0 (since edges are 0->1, reverse is 1->0? No).
    # Wait, the rule is: direct edges such that NO path of length >= 2 exists.
    # If we make the graph a bipartite graph with edges directed 0 -> 1:
    # Then any path is just a single edge (length 1).
    # Why? Because there are no edges starting from a node in set 1. All edges go into set 1.
    # So from any node in set 1, out-degree is 0. Thus no path of length 2 can start from a node in set 1.
    # Can a path of length 2 start from set 0? u(0) -> v(1) -> w(...). 
    # For v->w to exist, v must have an outgoing edge. But we directed all edges 0->1. So v (in 1) has no outgoing edges.
    # Thus, max path length is 1.
    
    result = []
    for u, v in edges:
        if color[u] == 0 and color[v] == 1:
            # Edge goes 0 -> 1, which is u -> v. 
            # Input says: '0' if u->v, '1' if v->u.
            result.append('0')
        else:
            # One is 0, one is 1. Must go 0 -> 1.
            # If u is 1 and v is 0, we need v -> u, which is '1'.
            # If u is 0 and v is 1, we need u -> v, which is '0'.
            if color[u] == 1 and color[v] == 0:
                result.append('1')
            else:
                # This case (u=0, v=1) is handled above.
                # What if both are same? Should not happen in bipartite graph.
                # Just in case logic falls through, but theoretically impossible.
                result.append('0')
    
    print("YES")
    print("".join(result))

if __name__ == '__main__':
    solve()