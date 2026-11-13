import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    try:
        N = int(next(iterator))
    except StopIteration:
        print(0)
        return
    
    if N < 3:
        print(0)
        return
    
    # Adjacency list
    adj = [[] for _ in range(N + 1)]
    
    for _ in range(N - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)
    
    # We need to count ordered paths of length 2: u -> v -> w
    # such that the shortest distance between u and w is exactly 2.
    # In a tree (which this graph is, since N nodes and N-1 edges and connected),
    # the distance between u and w is 2 if and only if they share a common neighbor v,
    # AND u != w.
    # The path u->v->w is optimal (shortest) if dist(u, w) == 2.
    # Since it's a tree, any path of length 2 between u and w via v implies dist(u,w)=2,
    # provided u != w. If u == w, dist(u,w)=0, so it's not 2.
    #
    # So we need to count triples (u, v, w) such that:
    # 1. (u, v) is an edge
    # 2. (v, w) is an edge
    # 3. u != w
    #
    # For a fixed center v, let deg(v) be the degree.
    # The number of ordered pairs (u, w) such that u and w are neighbors of v and u != w
    # is simply deg(v) * (deg(v) - 1).
    #
    # Summing this over all v gives the total count.

    total_paths = 0
    
    for v in range(1, N + 1):
        deg = len(adj[v])
        if deg >= 2:
            total_paths += deg * (deg - 1)
    
    print(total_paths)

if __name__ == "__main__":
    solve()