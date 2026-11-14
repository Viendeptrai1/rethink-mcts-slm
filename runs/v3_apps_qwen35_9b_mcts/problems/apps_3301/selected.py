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
        for _ in range(P):
            u = int(next(iterator))
            v = int(next(iterator))
            w = int(next(iterator))
            edges.append((u, v, w))
            edges.append((v, u, w))
            
        M = int(next(iterator))
        swerc_banks = set()
        for _ in range(M):
            swerc_banks.add(int(next(iterator)))
            
    except StopIteration:
        return

    # Build adjacency list
    adj = [[] for _ in range(N + 1)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    # Function to compute (min_hops, min_cost_for_min_hops) from start to end
    # Returns (hops, cost) or (inf, inf) if unreachable
    def get_best_path(start, end, allowed_banks):
        # allowed_banks is a set of nodes that can be used as intermediaries
        # Note: start and end are always allowed (they are in swerc_banks or given)
        # But for the "all banks" case, all banks 1..N are allowed.
        # For the "SWERC only" case, only nodes in allowed_banks are allowed.
        
        # We need the path with minimum hops. If multiple, the one with minimum sum of original weights.
        # State: (node, hops, cost)
        # We use Dijkstra-like approach where primary key is hops, secondary is cost.
        # However, since edge weights are positive, we can't simply use BFS for cost.
        # But we know the max hops is N. We can iterate on number of hops k from 0 to N.
        # For a fixed k, we want the min cost path with exactly k hops.
        # This is equivalent to finding the shortest path in a graph where all edges have weight 1 (for hops)
        # and we break ties with original weights.
        
        # Actually, standard approach: 
        # dist[node] = (min_hops, min_cost)
        # Initialize dist[start] = (0, 0), others = (inf, inf)
        # Priority queue: (hops, cost, u)
        
        pq = [(0, 0, start)]
        dist = {}
        dist[start] = (0, 0)
        
        while pq:
            h, c, u = heapq.heappop(pq)
            
            if (u, h, c) in dist.get(u, (float('inf'), float('inf'))):
                # Check if this state is worse than what we already found for u with <= h hops
                # Actually, we store best (h, c) for each node.
                # If we popped a state that is strictly worse than recorded, skip.
                if u in dist:
                    best_h, best_c = dist[u]
                    if h > best_h or (h == best_h and c > best_c):
                        continue
            
            if u == end:
                # Since we use a priority queue on (hops, cost), the first time we pop end,
                # it is guaranteed to be the optimal (min hops, then min cost).
                return h, c
            
            for v, w in adj[u]:
                if v not in allowed_banks:
                    continue
                
                new_h = h + 1
                new_c = c + w
                
                # Check if we found a better way to v
                if v not in dist:
                    dist[v] = (new_h, new_c)
                    heapq.heappush(pq, (new_h, new_c, v))
                else:
                    old_h, old_c = dist[v]
                    if new_h < old_h or (new_h == old_h and new_c < old_c):
                        dist[v] = (new_h, new_c)
                        heapq.heappush(pq, (new_h, new_c, v))
        
        return float('inf'), float('inf')

    # Case 1: All banks allowed
    h_all, c_all = get_best_path(X, Y, set(range(1, N + 1)))
    
    # Case 2: Only SWERC banks allowed
    h_swerc, c_swerc = get_best_path(X, Y, swerc_banks)
    
    # If SWERC cannot reach Y at all
    if h_swerc == float('inf'):
        print("Impossible")
        return
    
    # If all banks cannot reach Y at all (shouldn't happen if SWERC can, but theoretically)
    if h_all == float('inf'):
        # This case implies SWERC path exists but global path doesn't? Impossible.
        # Or maybe X/Y not connected in global graph? But SWERC path implies connectivity.
        print("Impossible")
        return

    # We want to find the largest fee K such that:
    # c_swerc + h_swerc * K <= c_all + h_all * K
    # c_swerc - c_all <= K * (h_all - h_swerc)
    
    diff_c = c_swerc - c_all
    diff_h = h_all - h_swerc
    
    # If diff_h == 0:
    #   Then we need c_swerc + h*K <= c_all + h*K => c_swerc <= c_all.
    #   If c_swerc <= c_all, then any K works -> Infinity.
    #   If c_swerc > c_all, then no K works -> Impossible.
    if diff_h == 0:
        if c_swerc <= c_all:
            print("Infinity")
        else:
            print("Impossible")
        return

    # If diff_h > 0:
    #   K * diff_h >= diff_c
    #   K >= diff_c / diff_h
    #   Since we want largest K? Wait.
    #   The condition is: SWERC path cost <= Global path cost.
    #   c_swerc + h_swerc * K <= c_all + h_all * K
    #   c_swerc - c_all <= K * (h_all - h_swerc)
    #   If h_all > h_swerc (diff_h > 0), then as K increases, RHS increases.
    #   So if the inequality holds for some K, it holds for all larger K.
    #   We want the LARGEST fee? 
    #   Re-reading the problem: "compute the largest fee so that SWERC can provide cheapest way"
    #   If SWERC is cheaper for large K, then SWERC is always cheaper for any K >= threshold.
    #   So the set of valid K is [threshold, infinity).
    #   The largest fee is Infinity.
    #   Wait, let's re-read carefully.
    #   "SWERC's goal is to provide the cheapest fees... She will try to lobby... so that the new fee makes this happen."
    #   "compute the largest fee so that SWERC can provide cheapest way"
    #   If for K=100, SWERC is cheapest. For K=1000, SWERC is cheapest.
    #   Then the answer is Infinity.
    #   If for K=10, SWERC is cheapest, but for K=11, Global becomes cheaper?
    #   That happens if h_swerc > h_all.
    #   Let's check the inequality direction again.
    #   Cost_SWERC(K) = c_swerc + h_swerc * K
    #   Cost_Global(K) = c_all + h_all * K
    #   We need Cost_SWERC(K) <= Cost_Global(K)
    #   c_swerc - c_all <= K * (h_all - h_swerc)
    
    # Scenario A: h_all > h_swerc (Global has more hops)
    #   RHS = K * positive.
    #   If c_swerc - c_all <= 0 (SWERC base cost lower or equal), then 0 <= positive*K is true for all K>=0. -> Infinity.
    #   If c_swerc - c_all > 0, then K >= (c_swerc - c_all) / (h_all - h_swerc).
    #   So for all K >= threshold, SWERC is cheaper. -> Infinity.
    #   Wait, is it possible that for small K, Global is cheaper, and for large K, SWERC is cheaper?
    #   Yes. If h_all > h_swerc, then Global path is more expensive in terms of hops.
    #   As K increases, the Global path cost grows faster. Eventually SWERC becomes cheaper.
    #   So if h_all > h_swerc, the answer is always Infinity?
    #   Unless... is there an upper bound on K? "largest fee". If it's always true for large K, then Infinity.
    #   But wait, what if c_swerc > c_all AND h_swerc > h_all?
    
    # Scenario B: h_swerc > h_all (SWERC has more hops)
    #   RHS = K * (negative number).
    #   Inequality: diff_c <= K * (-diff_h_pos)
    #   diff_c <= -K * diff_h_pos
    #   K * diff_h_pos <= -diff_c
    #   K <= -diff_c / diff_h_pos
    #   Here, K must be less than or equal to some value.
    #   We want the LARGEST fee. So the answer is floor(-diff_c / diff_h_pos).
    #   But we also need K >= 1 (fee > 0).
    #   If the calculated max K < 1, then Impossible.
    
    # Let's re-evaluate Scenario A (h_all > h_swerc).
    #   Inequality: K >= (c_swerc - c_all) / (h_all - h_swerc)
    #   This means for all K >= threshold, SWERC is optimal.
    #   The question asks for the "largest fee". If the set of valid fees is unbounded, output Infinity.
    #   Is it possible that for very large K, SWERC is NOT optimal?
    #   No, because SWERC has fewer hops, so its cost grows slower. It will eventually be strictly better.
    #   So if h_all > h_swerc, the answer is Infinity.
    
    # What if h_all == h_swerc?
    #   Then we need c_swerc <= c_all. If true -> Infinity. Else -> Impossible.
    
    # What if h_swerc > h_all?
    #   Then SWERC has more hops. As K increases, SWERC becomes more expensive relative to Global.
    #   There is a maximum K beyond which Global becomes cheaper.
    #   We need to find the largest integer K such that:
    #   c_swerc + h_swerc * K <= c_all + h_all * K
    #   c_swerc - c_all <= K * (h_all - h_swerc)
    #   Let D_h = h_all - h_swerc (which is negative).
    #   Let D_c = c_swerc - c_all.
    #   D_c <= K * D_h
    #   Since D_h < 0, dividing by D_h reverses inequality:
    #   K >= D_c / D_h  ??? No.
    #   Example: 10 <= K * (-2) => -5 >= K => K <= -5.
    #   So K <= D_c / D_h.
    #   Since D_h is negative, D_c / D_h might be positive or negative.
    #   We need K >= 1.
    #   So max K = floor(D_c / D_h).
    #   If max K < 1, then Impossible.
    
    # Summary:
    # 1. If h_swerc > h_all:
    #      max_K = floor((c_swerc - c_all) / (h_all - h_swerc))
    #      If max_K >= 1: print max_K
    #      Else: print "Impossible"
    # 2. If h_swerc <= h_all:
    #      # Inequality is K >= something.
    #      # So for all K >= threshold, it holds.
    #      # Thus largest fee is Infinity.
    #      print("Infinity")
    
    # Wait, let's double check the "h_swerc <= h_all" logic.
    # If h_swerc < h_all: SWERC has fewer hops.
    #   Cost_SWERC = c_swerc + h_swerc * K
    #   Cost_Global = c_all + h_all * K
    #   Diff = Cost_Global - Cost_SWERC = (c_all - c_swerc) + (h_all - h_swerc) * K
    #   Since (h_all - h_swerc) > 0, as K -> infinity, Diff -> infinity.
    #   So eventually Cost_Global > Cost_SWERC.
    #   So SWERC is optimal for all sufficiently large K. -> Infinity.
    # If h_swerc == h_all:
    #   Diff = c_all - c_swerc.
    #   If c_all >= c_swerc, Diff >= 0 always. -> Infinity.
    #   If c_all < c_swerc, Diff < 0 always. -> Impossible.
    
    # So the only case with a finite answer is h_swerc > h_all.
    
    if h_swerc > h_all:
        # h_all - h_swerc is negative
        numerator = c_swerc - c_all
        denominator = h_all - h_swerc # negative
        
        # We need K <= numerator / denominator
        # Since denominator is negative, let's make it positive for integer division logic
        # K <= numerator / denominator
        # Example: num=10, den=-2 => K <= -5.
        # Example: num=-10, den=-2 => K <= 5.
        
        # Integer division in Python: // floors.
        # We want floor(numerator / denominator).
        # But careful with negative numbers.
        # Python's // operator does floor division.
        # 10 // -2 = -5. Correct.
        # -10 // -2 = 5. Correct.
        # 10 // -3 = -4. (10/-3 = -3.33, floor is -4). Correct.
        
        max_k = numerator // denominator
        
        if max_k >= 1:
            print(max_k)
        else:
            print("Impossible")
    else:
        print("Infinity")

if __name__ == '__main__':
    solve()