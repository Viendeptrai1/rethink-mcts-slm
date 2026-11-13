import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    try:
        n = int(next(iterator))
    except StopIteration:
        return

    if n < 3:
        print(0)
        return

    adj = [[] for _ in range(n + 1)]
    
    for _ in range(n - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    count = 0
    for u in range(1, n + 1):
        neighbors = adj[u]
        m = len(neighbors)
        if m < 2:
            continue
        
        # Count pairs of neighbors that are connected
        # Since the graph is a tree, any two neighbors of u are connected
        # if and only if they share a common edge.
        # In a tree, if two neighbors v1 and v2 of u are connected,
        # then the path v1-u-v2 has length 2. The direct edge v1-v2 would make
        # a cycle of length 3, which is impossible in a tree unless v1 and v2
        # are the same node (impossible) or there is an edge between them.
        # But wait, the problem states the graph has N junctions and N-1 roads,
        # and each road connects two different junctions. This defines a tree.
        # In a tree, there are no cycles. Therefore, no two neighbors of u can be
        # directly connected by an edge.
        #
        # Re-reading the problem carefully:
        # "a Pokenom can run away to junction v, iff the optimal path between u and v has length exactly 2."
        # We need to count the number of such paths.
        # A path is defined as a sequence v0 -> v1 -> ... -> vK.
        # Here we are looking for paths of length 2: s -> w -> t.
        # The condition is that the optimal path between s and t has length exactly 2.
        # In a tree, the unique simple path between s and t is the optimal path.
        # So we need to count pairs (s, t) such that the unique path between them has length 2.
        # This means s and t are at distance 2 in the tree.
        # The number of such ordered pairs (s, t) is what we need.
        #
        # How to count pairs at distance 2?
        # For every node w, let deg(w) be its degree.
        # Any two distinct neighbors of w form a pair (s, t) such that the path s-w-t has length 2.
        # Since it's a tree, the path between s and t is unique and goes through w.
        # Thus, for each node w, the number of pairs (s, t) with s != t such that dist(s, t) = 2
        # and the middle node is w is deg(w) * (deg(w) - 1).
        #
        # We sum this over all nodes w.
        # Note: The path s -> w -> t is distinct from t -> w -> s.
        # The formula deg(w) * (deg(w) - 1) counts ordered pairs (s, t) where s != t.
        # Example: w has neighbors a, b, c.
        # Pairs: (a,b), (a,c), (b,a), (b,c), (c,a), (c,b). Total 3*2 = 6.
        # These correspond to paths: a->w->b, a->w->c, b->w->a, b->w->c, c->w->a, c->w->b.
        # All these have optimal length 2 because in a tree the path is unique.
        
        total_pairs = m * (m - 1)
        count += total_pairs

    print(count)

if __name__ == '__main__':
    solve()