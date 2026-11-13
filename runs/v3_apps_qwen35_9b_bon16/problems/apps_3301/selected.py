import sys
import heapq

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        P = int(next(iterator))
        X = int(next(iterator))
        Y = int(next(iterator))
        
        edges = []
        adj = [[] for _ in range(N + 1)]
        
        for _ in range(P):
            u = int(next(iterator))
            v = int(next(iterator))
            w = int(next(iterator))
            edges.append((u, v, w))
            adj[u].append((v, w))
            adj[v].append((u, w))
        
        M = int(next(iterator))
        swerc_banks = set()
        for _ in range(M):
            swerc_banks.add(int(next(iterator)))
            
    except StopIteration:
        return

    # Check if X and Y are in SWERC banks (problem says they are, but good to be safe)
    if X not in swerc_banks or Y not in swerc_banks:
        # According to problem statement, this shouldn't happen.
        # But if it did, we can't provide a path using only SWERC banks as intermediaries?
        # Actually, the problem says "using only its banks as intermediaries". 
        # X and Y are endpoints, they must be in the set. The path can go through non-SWERC banks?
        # Re-reading: "SWERC's goal is to provide the cheapest fees for its clients, using only its banks as intermediaries"
        # This implies the path from X to Y can ONLY use banks that are in the SWERC set (including X and Y).
        # If the graph of only SWERC banks has no path, then Impossible.
        print("Impossible")
        return

    # Build subgraph with only SWERC banks
    swerc_adj = [[] for _ in range(N + 1)]
    for u, v, w in edges:
        if u in swerc_banks and v in swerc_banks:
            swerc_adj[u].append((v, w))
            swerc_adj[v].append((u, w))

    # Function to find shortest path from X to Y in the subgraph
    def get_shortest_path(current_fee):
        # Dijkstra
        dist = {i: float('inf') for i in range(1, N + 1)}
        dist[X] = 0
        pq = [(0, X)]
        
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            if u == Y:
                return d
            
            for v, w in swerc_adj[u]:
                new_dist = d + w + current_fee
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    heapq.heappush(pq, (new_dist, v))
        return float('inf')

    # Binary search for the largest fee
    # Lower bound: 0 (or 1, since fee > 0)
    # Upper bound: max possible fee needed is bounded by max edge weight + something?
    # Actually, if fee is very large, the path with fewer edges is better.
    # The worst case is when the direct edge (if exists) or the path with min edges is optimal.
    # The fee can be up to 10^9. Let's set upper bound high enough.
    # Max edge weight is 10^9. Max number of edges in simple path is N.
    # If fee is 10^18, then any path with > 1 edge will be worse than direct if direct exists.
    # Let's use 2 * 10^9 + 7 as a safe upper bound for binary search, or just 10^18.
    
    # However, we need to check if there exists ANY fee > 0 such that SWERC path is strictly cheaper.
    # We are looking for the LARGEST fee F such that:
    # cost_swerc(F) < cost_best(F)
    # where cost_swerc(F) is the shortest path using only SWERC banks with edge cost = w + F
    # and cost_best(F) is the shortest path using ANY banks with edge cost = w + F.
    
    # Note: The problem says "largest fee so that SWERC can provide cheapest way".
    # This implies strictly cheaper.
    
    # Algorithm:
    # 1. Find the shortest path in the full graph (all banks) with fee F.
    # 2. Find the shortest path in the SWERC subgraph (only SWERC banks) with fee F.
    # 3. We need max F such that dist_swerc(F) < dist_full(F).
    
    # As F increases, both distances increase linearly with slope = number of edges in the path.
    # Let path_swerc have E_s edges and total base weight W_s. Cost = E_s * F + W_s.
    # Let path_full have E_f edges and total base weight W_f. Cost = E_f * F + W_f.
    # We need E_s * F + W_s < E_f * F + W_f
    # => F * (E_s - E_f) < W_f - W_s
    # 
    # Case 1: E_s < E_f. Then F * (negative) < (W_f - W_s). 
    # If W_f - W_s > 0, then inequality holds for all F >= 0. Answer Infinity.
    # If W_f - W_s <= 0, then F * (negative) <= negative. Since F >= 0, LHS <= 0, RHS <= 0.
    # Wait, if E_s < E_f, then as F -> infinity, LHS -> -infinity, RHS is constant.
    # Inequality: -k * F < C. If k > 0, for large F, -kF is very negative, so inequality holds.
    # So if E_s < E_f, SWERC path has fewer hops. For large F, SWERC path is better.
    # Unless W_f - W_s is such that it doesn't hold for small F?
    # Actually, if E_s < E_f, then for sufficiently large F, SWERC path is always cheaper.
    # So if there exists any path in SWERC subgraph and it has fewer edges than the best path in full graph
    # for large F, then Infinity.
    # Specifically, let min_edges_full be the minimum number of edges in any path from X to Y in full graph.
    # Let min_edges_swerc be the minimum number of edges in any path from X to Y in SWERC subgraph.
    # If min_edges_swerc < min_edges_full, then as F -> infinity, the SWERC path (with fewer edges) will dominate.
    # Because Cost_swerc ~ E_s * F, Cost_full ~ E_f * F. If E_s < E_f, Cost_swerc < Cost_full for large F.
    # So answer is Infinity.
    # But we must ensure that a path exists in SWERC subgraph.
    
    # Case 2: E_s == E_f.
    # Then we need W_s < W_f.
    # If W_s < W_f, then inequality holds for all F >= 0. Answer Infinity.
    # If W_s >= W_f, then inequality never holds (since F >= 0, LHS >= RHS if W_s >= W_f? No)
    # F * 0 + W_s < F * 0 + W_f => W_s < W_f. If not, impossible.
    
    # Case 3: E_s > E_f.
    # Then F * (E_s - E_f) < W_f - W_s
    # F < (W_f - W_s) / (E_s - E_f)
    # We need the largest integer F satisfying this.
    # Also F must be > 0.
    # If W_f - W_s <= 0, then no positive F satisfies (since LHS >= 0, RHS <= 0). Impossible.
    # Otherwise, F < (W_f - W_s) / (E_s - E_f).
    # Max integer F = floor((W_f - W_s - 1) / (E_s - E_f))? 
    # Strict inequality: F * D < Diff => F <= (Diff - 1) // D.
    
    # So strategy:
    # 1. Find the path in full graph with minimum number of edges. Let this be (E_min_full, W_min_full).
    #    Actually, we need to consider that for a given F, the shortest path might change.
    #    However, for very large F, the shortest path in the full graph will be one with the MINIMUM number of edges.
    #    Similarly for SWERC subgraph.
    #    
    #    Let's denote:
    #    P_full_min_edges: the path in full graph with minimum number of edges from X to Y.
    #    P_swerc_min_edges: the path in SWERC subgraph with minimum number of edges from X to Y.
    #    
    #    If no path in SWERC subgraph exists -> Impossible.
    #    
    #    Let E_s = len(P_swerc_min_edges), W_s = sum of base weights of P_swerc_min_edges.
    #    Let E_f = len(P_full_min_edges), W_f = sum of base weights of P_full_min_edges.
    #    
    #    Wait, is it sufficient to only compare the minimum edge paths?
    #    Suppose for some F, the best full path has E_f edges and weight W_f, and best swerc has E_s edges and weight W_s.
    #    As F increases, the relative order of paths depends on the number of edges.
    #    The path with the minimum number of edges will eventually become the unique shortest path (or one of them) for large F.
    #    So we can just compare the "limit" paths.
    #    
    #    If E_s < E_f: Infinity (provided SWERC path exists).
    #    If E_s == E_f:
    #        If W_s < W_f: Infinity.
    #        Else: Impossible.
    #    If E_s > E_f:
    #        We need F < (W_f - W_s) / (E_s - E_f).
    #        Let Num = W_f - W_s, Den = E_s - E_f.
    #        If Num <= 0: Impossible.
    #        Else: Max F = (Num - 1) // Den.
    #        If Max F <= 0: Impossible (since fee must be > 0).
    
    # How to find the path with minimum number of edges and minimum weight among those?
    # Actually, for the "Infinity" case, we need to know if there exists ANY path in SWERC with fewer edges than the BEST path in FULL for large F.
    # The best path in FULL for large F is the one with minimum edges.
    # Similarly for SWERC.
    # So we need:
    # 1. Shortest path in terms of number of edges in full graph.
    # 2. Shortest path in terms of number of edges in SWERC subgraph.
    # But if there are multiple paths with the same minimum number of edges, we need the one with minimum base weight.
    # So:
    # For full graph: Find path with min edges. Among those, min weight. -> (E_f, W_f)
    # For SWERC graph: Find path with min edges. Among those, min weight. -> (E_s, W_s)
    
    # Algorithm to find (min_edges, min_weight_for_those_edges):
    # BFS to find min edges.
    # Then use Dijkstra/BFS on layers? Or just:
    # Run BFS to compute min_edges[u] for all u.
    # Then we want the path from X to Y with min_edges[Y] edges and minimum sum of weights.
    # This can be done by relaxing edges in increasing order of edges (Dial's algorithm or just BFS + DP).
    # Actually, simpler:
    # 1. BFS to get min_dist_edges[u] = min edges from X to u.
    # 2. Then run a shortest path algorithm where edge weight is (1, w). Compare by edges first, then weight.
    #    This is equivalent to finding the path with lexicographically smallest (edges, weight).
    #    We can use Dijkstra with custom comparator: (edges, weight).
    #    Since edges are non-negative, Dijkstra works.
    
    # Let's implement a Dijkstra that returns (edges, weight) for the shortest path.
    # Compare (e1, w1) < (e2, w2) if e1 < e2 or (e1 == e2 and w1 < w2).
    
    def get_best_path_metric(adj, start, end):
        # Returns (edges, weight) of the path that minimizes edges, then weight.
        # If end is not reachable, return (inf, inf)
        n = len(adj) - 1
        dist_edges = {i: float('inf') for i in range(1, n + 1)}
        dist_weight = {i: float('inf') for i in range(1, n + 1)}
        dist_edges[start] = 0
        dist_weight[start] = 0
        
        # Priority queue: (edges, weight, u)
        pq = [(0, 0, start)]
        
        while pq:
            e, w, u = heapq.heappop(pq)
            if e > dist_edges[u]:
                continue
            if e == dist_edges[u] and w > dist_weight[u]:
                continue
            
            if u == end:
                return (e, w)
            
            for v, weight in adj[u]:
                new_e = e + 1
                new_w = w + weight
                if new_e < dist_edges[v]:
                    dist_edges[v] = new_e
                    dist_weight[v] = new_w
                    heapq.heappush(pq, (new_e, new_w, v))
                elif new_e == dist_edges[v] and new_w < dist_weight[v]:
                    dist_weight[v] = new_w
                    heapq.heappush(pq, (new_e, new_w, v))
        return (float('inf'), float('inf'))

    full_res = get_best_path_metric(adj, X, Y)
    swerc_res = get_best_path_metric(swerc_adj, X, Y)
    
    full_edges, full_weight = full_res
    swerc_edges, swerc_weight = swerc_res
    
    if swerc_edges == float('inf'):
        print("Impossible")
        return
    
    # Compare
    if swerc_edges < full_edges:
        print("Infinity")
    elif swerc_edges == full_edges:
        if swerc_weight < full_weight:
            print("Infinity")
        else:
            print("Impossible")
    else:
        # swerc_edges > full_edges
        diff_w = full_weight - swerc_weight
        diff_e = swerc_edges - full_edges
        
        if diff_w <= 0:
            print("Impossible")
        else:
            # F < diff_w / diff_e
            # Max integer F = (diff_w - 1) // diff_e
            ans = (diff_w - 1) // diff_e
            if ans > 0:
                print(ans)
            else:
                print("Impossible")

if __name__ == '__main__':
    solve()