import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    current_time = 0
    current_zone = 0
    min_coupons = 0

    # State: (valid_until, zone_coverage_start, zone_coverage_end)
    # We want to maximize the coverage interval [A, B] such that:
    # 1. The ticket is valid at current_time (i.e., valid_until >= current_time)
    # 2. The ticket covers the current trip zone (i.e., A <= current_zone <= B)
    # 3. The cost 2 + |A-B| is minimized.
    
    # Since N is up to 400,000, we need an efficient way to query the best previous ticket.
    # The state space for zones is small (0 to 10). We can maintain the best valid ticket 
    # for every possible interval ending time? No, that's too many.
    # However, the number of possible intervals [A, B] is small: 11*11/2 = 66.
    # We can maintain the "last expiration time" for each possible ticket interval [A, B].
    # When a new trip comes at time T in zone Z, we check all 66 intervals [A, B] that cover Z.
    # If an interval [A, B] was purchased last at time last_used[A][B] and last_used[A][B] + 10000 >= T,
    # then this ticket is still valid. We pick the one with minimal cost.
    
    # Initialize last_used for all intervals to -1 (or sufficiently small)
    # Zones are 0..10.
    last_used = {}
    # Precompute all intervals [A, B] where 0 <= A <= B <= 10
    intervals = []
    for A in range(11):
        for B in range(A, 11):
            intervals.append((A, B))
    
    # Map from interval to its last used time
    last_used = { (A, B): -float('inf') for A, B in intervals }
    
    for _ in range(N):
        Z = int(next(iterator))
        T = int(next(iterator))
        
        best_cost = float('inf')
        best_interval = None
        
        # Check all intervals that cover Z
        for A, B in intervals:
            if A <= Z <= B:
                cost = 2 + (B - A)
                last_used_time = last_used[(A, B)]
                if last_used_time + 10000 >= T:
                    if cost < best_cost:
                        best_cost = cost
                        best_interval = (A, B)
        
        if best_interval is None:
            # Must buy a new ticket.
            # To minimize cost, we should buy the cheapest ticket that covers Z.
            # Cheapest is when A=B=Z, cost = 2.
            min_cost = 2
            # But wait, maybe buying a larger ticket is not more expensive?
            # Cost = 2 + |A-B|. Minimum is when |A-B| is 0. So cost 2.
            # So we just buy [Z, Z].
            new_interval = (Z, Z)
            min_coupons += min_cost
            last_used[new_interval] = T
        else:
            # Use existing ticket
            min_coupons += best_cost
            # Update the last used time for this interval to current T
            last_used[best_interval] = T

    print(min_coupons)

if __name__ == "__main__":
    solve()