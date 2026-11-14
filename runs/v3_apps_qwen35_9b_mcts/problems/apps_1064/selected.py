import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)

    try:
        n = int(next(iterator))
        m = int(next(iterator))
        k = int(next(iterator))
        
        blocked = set()
        for _ in range(m):
            blocked.add(int(next(iterator)))
            
        costs = []
        for _ in range(k):
            costs.append(int(next(iterator)))
    except StopIteration:
        return

    # Precompute next_valid[i]: the smallest index >= i that is not blocked
    # If all positions from i to n-1 are blocked, next_valid[i] = n (or infinity)
    # We need to cover [0, n]. The lamp at x covers [x, x+l].
    # We need to reach position n.
    
    # Let's create an array `next_unblocked` where next_unblocked[i] is the first non-blocked position >= i.
    # If i >= n, it's effectively covered or irrelevant for starting a lamp, but we need to reach n.
    # Actually, the condition is: we are at current position `curr` (initially 0).
    # We need to place a lamp at some position `p` such that `p >= curr` and `p` is not blocked.
    # The lamp covers [p, p+l]. We want to maximize p+l to jump as far as possible.
    # So from `curr`, we find the largest `p` such that `p >= curr`, `p` is not blocked, and `p + l <= n`? 
    # No, the problem says: "he may place a lamp of power 3 in position n - 1 (even though its illumination zone doesn't completely belong to segment [0, n])".
    # So we can place a lamp at any non-blocked position p >= curr.
    # The coverage is [p, p+l]. We need the union of these intervals to cover [0, n].
    # Greedy strategy: from current uncovered position `curr`, pick the largest valid `p` (non-blocked, p >= curr) such that we can make progress.
    # Actually, to maximize the reach, we should pick the largest `p` such that `p` is not blocked and `p >= curr`.
    # Wait, if we pick a very large `p`, the interval starts late. We need to cover `curr`.
    # So we must have `p <= curr + l`? No, the lamp is placed at `p` and covers `[p, p+l]`.
    # To cover `curr`, we need `p <= curr`. But we are at `curr` meaning everything before `curr` is covered.
    # So we need to cover `curr`. The lamp placed at `p` covers `[p, p+l]`.
    # If `p > curr`, then `curr` is not covered by this lamp.
    # Therefore, we MUST place the lamp at some `p` such that `p <= curr`.
    # But we also need `p` to be a valid position (not blocked) and `p >= 0`.
    # And since we are progressing from left to right, we usually look for `p` in the range `[curr - l + 1, curr]`?
    # Let's re-read carefully: "When placed in position x, post lamp of power l illuminates the segment [x; x + l]."
    # We are at state: positions [0, curr) are covered. We need to cover `curr`.
    # We need to place a lamp at some position `x` such that `x <= curr` (to cover `curr`) and `x` is not blocked.
    # To maximize the new covered range, we want to maximize `x + l`.
    # Since `l` is fixed for a specific lamp type, maximizing `x + l` is equivalent to maximizing `x`.
    # So we need the largest `x` such that `x <= curr`, `x` is not blocked, and `x >= 0`.
    # However, there is a constraint: we can only place lamps at positions `0` to `n-1`.
    # So `x` must be in `[0, n-1]`.
    # Also, if the largest valid `x` is less than `curr - l + 1`, then the interval `[x, x+l]` ends before `curr`?
    # No, if `x <= curr`, then `x + l >= curr + l > curr`. So `curr` is always covered if `x <= curr`.
    # The only issue is if no such `x` exists (i.e., all positions in `[0, curr]` are blocked). Then we can't cover `curr`.
    
    # Algorithm for a fixed lamp power `l`:
    # curr = 0
    # cost = 0
    # while curr < n:
    #   Find largest x such that x <= curr, x < n, x not in blocked.
    #   If no such x exists (i.e., all positions in [0, curr] are blocked), then impossible.
    #   Actually, we need to cover `curr`. The lamp at `x` covers `[x, x+l]`.
    #   We need `x <= curr`.
    #   To maximize reach, we pick largest such `x`.
    #   New covered end = x + l.
    #   If new covered end <= curr, we made no progress -> impossible (unless curr >= n).
    #   curr = new covered end.
    #   cost += cost[l-1]
    # If loop finishes with curr >= n, return cost.
    
    # Optimization:
    # Instead of scanning backwards for every step, we can precompute `prev_unblocked[i]`:
    # the largest non-blocked position <= i.
    # Then for a given `curr`, the best `x` is `prev_unblocked[curr]`.
    # If `prev_unblocked[curr]` does not exist (i.e., all 0..curr are blocked), then fail.
    # Note: positions are 0 to n-1.
    # If `curr` reaches `n`, we are done.
    
    # Precompute prev_unblocked array of size n+1.
    # prev_unblocked[i] = largest j <= i such that j is not blocked.
    # If no such j exists, store -1.
    
    prev_unblocked = [-1] * (n + 1)
    last_valid = -1
    for i in range(n):
        if i not in blocked:
            last_valid = i
        prev_unblocked[i] = last_valid
    # For i >= n, we don't really need it, but let's handle the logic.
    # When curr == n, we stop.
    # When curr < n, we look at prev_unblocked[curr].
    
    min_total_cost = float('inf')
    
    # We need to simulate for each lamp type l from 1 to k.
    # Complexity: O(n + k * (n/l))? In worst case l=1, O(n*k) which is 10^12. Too slow.
    # We need a faster way.
    
    # Observation:
    # For a fixed l, the process is deterministic.
    # curr_0 = 0
    # x_0 = prev_unblocked[curr_0]
    # curr_1 = x_0 + l
    # x_1 = prev_unblocked[curr_1]
    # curr_2 = x_1 + l
    # ...
    # This looks like we are jumping.
    # Can we optimize the simulation?
    # Notice that x_i = prev_unblocked[curr_i].
    # curr_{i+1} = prev_unblocked[curr_i] + l.
    # This is a functional graph traversal.
    # Since n is up to 10^6 and k up to 10^6, we cannot simulate each l separately if the path is long.
    # However, note that if l is large, the number of steps is small (n/l).
    # If l is small, the number of steps is large, but maybe we can skip?
    # Actually, the total complexity over all l might be acceptable if we are careful?
    # Sum of n/l for l=1 to k is n * H_k approx n ln k.
    # 10^6 * ln(10^6) approx 10^6 * 14 = 1.4 * 10^7. This is acceptable!
    # So simple simulation for each l is O(n log k) or O(n) total?
    # Wait, the step size is not exactly l. The jump is: curr -> prev_unblocked[curr] + l.
    # The value `prev_unblocked[curr]` is <= curr.
    # So the new curr is `prev_unblocked[curr] + l`.
    # The decrease in curr is `curr - prev_unblocked[curr]`. This is the distance to the previous unblocked spot.
    # Let `gap[i] = i - prev_unblocked[i]`. If `prev_unblocked[i] == -1`, gap is infinity.
    # Then curr_{new} = curr - gap[curr] + l.
    # We need curr_{new} > curr to make progress. So l > gap[curr].
    # If l <= gap[curr], we get stuck or move back?
    # If l <= gap[curr], then curr_{new} = curr - gap + l <= curr.
    # If curr_{new} <= curr, we are not making progress towards n.
    # Specifically, if curr_{new} <= curr, and we are in a loop or stuck, we fail.
    # Actually, if curr_{new} <= curr, we haven't covered anything new beyond `curr`.
    # Since we need to cover `curr`, and the new coverage ends at `curr_{new}`, if `curr_{new} <= curr`, we failed to extend coverage.
    # So condition: if `prev_unblocked[curr] + l <= curr`, then impossible.
    
    # So the simulation is:
    # curr = 0
    # while curr < n:
    #   p = prev_unblocked[curr]
    #   if p == -1: return impossible
    #   if p + l <= curr: return impossible
    #   curr = p + l
    #   cost += a[l-1]
    
    # Total steps across all l:
    # In the worst case, for small l, we take many steps.
    # But notice that `curr` increases by at least 1 each step (since p >= curr - (l-1) is not guaranteed, but p+ l > curr implies increase).
    # Actually, the number of steps is at most n.
    # So total complexity is sum_{l=1}^k (n/l) = O(n log k).
    # With n=10^6, k=10^6, n log k ~ 1.4e7 operations. This fits within 1-2 seconds in Python if implemented efficiently.
    
    # Let's implement this.
    
    # Precompute prev_unblocked
    # blocked set is already built.
    
    # To speed up, we can convert blocked set to a boolean array or use the set directly.
    # Array lookup is faster.
    is_blocked = [False] * n
    for b in blocked:
        is_blocked[b] = True
        
    # Build prev_unblocked
    # We can do this in one pass.
    prev_unblocked = [-1] * (n + 1)
    last = -1
    for i in range(n):
        if not is_blocked[i]:
            last = i
        prev_unblocked[i] = last
    # prev_unblocked[n] is not strictly needed as loop condition is curr < n.
    
    ans = float('inf')
    
    # Iterate l from 1 to k
    for l in range(1, k + 1):
        cost_l = costs[l-1]
        if cost_l >= ans:
            # Since costs are positive, if current cost per lamp is already >= best found,
            # and we need at least 1 lamp, we can't beat ans unless we need 0 lamps (impossible as n>=1).
            # But wait, we might need fewer lamps if l is larger?
            # No, cost_l is the price of ONE lamp. If cost_l >= ans, then even 1 lamp is too expensive.
            # So we can skip.
            continue
            
        curr = 0
        possible = True
        steps = 0
        while curr < n:
            p = prev_unblocked[curr]
            if p == -1:
                possible = False
                break
            if p + l <= curr:
                possible = False
                break
            curr = p + l
            steps += 1
            if steps * cost_l >= ans:
                # Optimization: if accumulated cost exceeds current best, break early
                possible = False
                break
        
        if possible:
            total = steps * cost_l
            if total < ans:
                ans = total
                
    if ans == float('inf'):
        print(-1)
    else:
        print(ans)

if __name__ == '__main__':
    solve()