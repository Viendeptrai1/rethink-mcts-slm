import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    idx = 0
    
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    k = int(data[idx]); idx += 1
    
    blocked = [False] * n
    for _ in range(m):
        pos = int(data[idx]); idx += 1
        blocked[pos] = True
    
    costs = [0] * (k + 1)
    for i in range(1, k + 1):
        costs[i] = int(data[idx]); idx += 1
    
    # Precompute best cost for each power: best_cost[p] = min(costs[p], best_cost[p-1] * something?)
    # Actually, we can cover distance D with power p by ceil(D/p) lamps.
    # But we are restricted to using EXACTLY ONE type.
    # So for a fixed power p, we need to find the min number of lamps to cover [0, n].
    # Then answer = min over p in [1, k] of (costs[p] * num_lamps[p]).
    
    # We need an efficient way to calculate min lamps for each power.
    # Since n is up to 10^6 and k up to 10^6, O(n*k) is too slow.
    # We can compute DP: dp[i] = min lamps to cover [0, i].
    # But the jump size depends on power.
    # However, note that if we fix the power p, then from position i (illuminated), 
    # we can jump to i + p, i + p - 1, ... i + 1 as long as the landing spot is not blocked.
    # Actually, the rule is: place lamp at x, covers [x, x+p].
    # To cover continuously from 0 to n, we need:
    # Start at 0. Place lamp at some x0 in [0, p-1] (if not blocked) such that x0+p > 0 (always true) and x0 >= 0.
    # Actually, to cover [0, n], we need the union of [x_i, x_i + p] to cover [0, n].
    # This implies we need a sequence of positions x_0, x_1, ... such that:
    # x_0 >= 0
    # x_{i+1} <= x_i + p  (overlap required)
    # x_i is not blocked
    # x_last + p >= n
    # And we want to minimize the number of lamps.
    # This is equivalent to: starting from current covered up to 'curr', what is the furthest we can reach?
    # No, it's greedy: to cover [0, n], we must start covering from 0.
    # The first lamp must be placed at some x in [0, p-1] (since if x >= p, 0 is not covered).
    # To maximize reach, we should pick the largest valid x in [0, min(p-1, n-1)] that is not blocked.
    # Let this be next_start. Then it covers up to next_start + p.
    # The next lamp must be placed at some x' in [next_start - (p-1), next_start] (to ensure continuity)
    # Actually, the condition is: the new lamp must start at x' such that x' <= current_reach (to cover the gap)
    # and we want to maximize x' + p.
    # So from current_reach, we look for the largest x' in [current_reach - p + 1, current_reach] that is not blocked.
    # If no such x' exists, then impossible for this power.
    
    # Algorithm for a fixed power p:
    # current_reach = 0
    # count = 0
    # while current_reach < n:
    #    We need to pick x' in [current_reach - p + 1, current_reach] such that x' is not blocked and x' >= 0.
    #    To maximize extension, pick largest such x'.
    #    If no such x', return infinity.
    #    new_reach = x' + p
    #    if new_reach <= current_reach: impossible (infinite loop or dead end)
    #    count += 1
    #    current_reach = new_reach
    # return count
    
    # To make this fast for all p, we can precompute "previous non-blocked" array.
    # Let prev_not_blocked[i] be the largest index j <= i such that blocked[j] is False.
    # Then for a given current_reach and power p, the candidate interval is [L, R] where R = current_reach, L = max(0, current_reach - p + 1).
    # We need the largest non-blocked in [L, R]. This is simply min(R, prev_not_blocked[R]).
    # If this value < L, then no valid spot exists -> impossible.
    # Otherwise, next_x = min(R, prev_not_blocked[R]), next_reach = next_x + p.
    
    # Precompute prev_not_blocked
    prev_not_blocked = [0] * n
    last = -1
    for i in range(n):
        if not blocked[i]:
            last = i
        prev_not_blocked[i] = last
    
    # Now iterate p from 1 to k
    min_total_cost = float('inf')
    possible = False
    
    for p in range(1, k + 1):
        cost = costs[p]
        current_reach = 0
        count = 0
        
        # We need to cover [0, n]. 
        # The loop continues as long as we haven't covered up to n.
        # But careful: if current_reach >= n, we are done.
        # However, the first lamp must cover 0.
        # If p >= 1, the interval for first lamp start is [0, min(p-1, n-1)].
        # If n=0? Problem says n>=1.
        
        while current_reach < n:
            # Determine the range of valid start positions for the next lamp
            # Must be <= current_reach to cover the gap starting at current_reach - epsilon
            # Must be >= current_reach - p + 1 to extend coverage by p
            # Must be >= 0
            lower = current_reach - p + 1
            if lower < 0:
                lower = 0
            upper = current_reach
            
            # Find largest non-blocked in [lower, upper]
            # If upper >= n, we can clamp upper to n-1 because positions are 0..n-1
            if upper >= n:
                upper = n - 1
            
            # If lower > upper, then no valid position exists (interval empty)
            if lower > upper:
                break # Impossible
            
            best_x = prev_not_blocked[upper]
            if best_x < lower:
                break # Impossible
            
            current_reach = best_x + p
            count += 1
            if count > 2 * n: # Safety break for infinite loop
                break
        
        if current_reach >= n:
            total_cost = count * cost
            if total_cost < min_total_cost:
                min_total_cost = total_cost
            possible = True
    
    if possible:
        print(min_total_cost)
    else:
        print(-1)

if __name__ == "__main__":
    solve()