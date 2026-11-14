import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    N = int(data[0])
    robots = []
    idx = 1
    for i in range(N):
        x = int(data[idx])
        d = int(data[idx+1])
        robots.append({'id': i, 'x': x, 'd': d})
        idx += 2
    
    # Sort robots by coordinate
    robots.sort(key=lambda r: r['x'])
    
    MOD = 998244353
    
    # We will process robots from right to left (largest x to smallest x)
    # For each robot i, we want to compute:
    # dp[i] = number of valid subsets of robots in the range [i, N-1] (in sorted order)
    # such that if we consider the dependency graph restricted to these robots,
    # the set is "closed" (if a robot is in the set, all its triggered robots are also in the set).
    # However, the problem asks for the number of possible REMAINING sets.
    # A set S remains if and only if S is a closed set in the dependency graph.
    # Actually, let's re-read carefully.
    # "How many possible sets of robots remaining on the number line"
    # If we activate a set of robots A, the final remaining set is the set of robots NOT activated.
    # Let U be the set of all robots. Let A be the set of activated robots.
    # The process is: start with A_0 = {initially chosen robots}.
    # Then repeatedly add j to A if i in A and i triggers j.
    # The final set of activated robots is the closure of A_0.
    # The remaining set is U \ closure(A_0).
    # We need to count the number of distinct sets R = U \ closure(A_0) as A_0 varies over all subsets of U.
    # Note that R is a valid remaining set if and only if R is a "closed" set in the sense that:
    # If a robot j is NOT in R (i.e., j is activated), then any robot i that triggers j must also be activated?
    # No, that's not the condition.
    # Let's define the dependency: i -> j if activating i triggers j.
    # If we activate a set A, the final activated set is the smallest set containing A and closed under the dependency.
    # Let C(A) be this closure. The remaining set is U \ C(A).
    # We want to count the number of distinct sets of the form U \ C(A).
    # Let R be a remaining set. Then R = U \ C(A) for some A.
    # This implies C(A) = U \ R.
    # For R to be a valid remaining set, there must exist an A such that C(A) = U \ R.
    # Note that C(A) is always a "closed" set in the dependency graph (if i in C(A) and i->j, then j in C(A)).
    # Also, for any closed set K, we can choose A = K, then C(K) = K.
    # So the set of possible remaining sets is exactly { U \ K | K is a closed set in the dependency graph }.
    # Since the mapping K -> U \ K is a bijection, the number of possible remaining sets is equal to the number of closed sets in the dependency graph.
    
    # So the problem reduces to: Count the number of closed sets in the dependency graph.
    # Dependency: i -> j if x_i <= x_j < x_i + d_i.
    # Since robots are sorted by x, for a robot i, it triggers a contiguous range of robots j > i (in sorted order)
    # such that x_j < x_i + d_i.
    # Let's denote the range of robots triggered by i as [i+1, r_i] (indices in the sorted array).
    # If no robot is triggered, r_i = i.
    
    # We can compute r_i for each i.
    # Since x_i are sorted, we can use binary search (bisect_right) to find the largest index j such that x_j < x_i + d_i.
    # Then the range is [i+1, j].
    
    # Now we have a DAG where each node i has edges to [i+1, r_i].
    # We need to count the number of closed sets.
    # A set S is closed if for all i in S, if i triggers j, then j in S.
    # This is equivalent to: if i in S and i+1 <= j <= r_i, then j in S.
    # We can use DP from right to left (N-1 down to 0).
    # Let dp[i] be the number of closed sets formed using robots from index i to N-1.
    # Consider robot i.
    # Case 1: Robot i is NOT in the closed set.
    #   Then any robot j > i can be in the set or not, as long as the subset of {i+1, ..., N-1} is closed.
    #   So we have dp[i+1] ways.
    # Case 2: Robot i IS in the closed set.
    #   Then all robots triggered by i must be in the set.
    #   The robots triggered by i are in the range [i+1, r_i].
    #   So robots i+1, i+2, ..., r_i MUST be in the set.
    #   Robots in the range [r_i+1, N-1] can be chosen freely as long as they form a closed set among themselves.
    #   So we have dp[r_i+1] ways.
    #   Note: if r_i = N-1, then dp[N] = 1 (empty set of further robots).
    #   If r_i < i+1 (no robots triggered), then we have dp[i+1] ways.
    
    # So:
    # dp[i] = dp[i+1] (if i not in set) + dp[r_i+1] (if i in set)
    # Base case: dp[N] = 1.
    
    # Let's verify with Sample 1:
    # N=2
    # Robot 0: x=1, d=5 -> range [1, 1+5) = [1, 6). Robots with x in [1, 6) are robot 1 (x=3).
    #   So robot 0 triggers robot 1. r_0 = 1.
    # Robot 1: x=3, d=3 -> range [3, 6). No robots > 1 in this range. r_1 = 1.
    #
    # dp[2] = 1
    # dp[1]: 
    #   i=1 not in set: dp[2] = 1
    #   i=1 in set: triggers nothing, so dp[r_1+1] = dp[2] = 1
    #   dp[1] = 1 + 1 = 2.
    # dp[0]:
    #   i=0 not in set: dp[1] = 2
    #   i=0 in set: triggers [1, 1], so must include 1. dp[r_0+1] = dp[2] = 1.
    #   dp[0] = 2 + 1 = 3.
    # Result 3. Matches sample.
    
    # Implementation details:
    # 1. Sort robots.
    # 2. For each i, find r_i using bisect_right on x coordinates.
    #    We need an array of x coordinates for bisect.
    # 3. Compute dp array from N-1 down to 0.
    
    import bisect
    
    xs = [r['x'] for r in robots]
    
    # Precompute r_i
    r = [0] * N
    for i in range(N):
        # Find largest index j such that xs[j] < xs[i] + robots[i]['d']
        limit = xs[i] + robots[i]['d']
        # bisect_right returns an insertion point i such that all e in a[:i] have e <= x
        # We want strictly less than limit.
        # bisect_right returns index where all elements to left are <= limit-1 (if integers)
        # Actually bisect_right(a, x) returns index after the last element <= x.
        # We want elements < limit. Since coordinates are integers, < limit is same as <= limit-1.
        # But bisect_right with 'limit' gives index after last element <= limit.
        # We want index after last element < limit.
        # Since xs are integers, < limit is equivalent to <= limit-1.
        # So we can use bisect_right with limit-1? 
        # Wait, if limit is 6, we want x < 6. Integers 1, 2, 3, 4, 5 are ok. 6 is not.
        # bisect_right(xs, 5) gives index after last 5.
        # bisect_right(xs, 6) gives index after last 6.
        # If there is a 6, bisect_right(6) includes it, bisect_right(5) excludes it.
        # So we should use bisect_right with limit-1? 
        # Example: xs = [1, 3], limit = 6. We want indices where x < 6. Both 1 and 3.
        # bisect_right([1,3], 5) -> 2. Correct.
        # bisect_right([1,3], 6) -> 2. Correct.
        # Example: xs = [1, 6], limit = 6. We want x < 6. Only 1.
        # bisect_right([1,6], 5) -> 1. Correct.
        # bisect_right([1,6], 6) -> 2. Incorrect (includes 6).
        # So we must use limit-1? 
        # But what if limit is very large? limit-1 is fine.
        # What if limit is negative? Constraints say D_i >= 1, X_i can be negative.
        # limit = X_i + D_i.
        # We want x < limit.
        # bisect_right returns index i such that all a[:i] <= x.
        # We want all a[:k] < limit.
        # Since values are integers, x < limit <=> x <= limit - 1.
        # So we can use bisect_right(xs, limit - 1).
        # However, if limit is very small (e.g. limit = -10^9), limit-1 is fine.
        # Is it possible that limit-1 overflows? Python handles large integers.
        # But wait, if limit is not an integer? No, inputs are integers.
        # So yes, use limit - 1.
        
        # Actually, simpler: bisect_left gives first index >= limit.
        # Then all indices < that index are < limit.
        # So r_i = bisect_left(xs, limit) - 1?
        # No, bisect_left returns the first index where xs[idx] >= limit.
        # So indices 0 to idx-1 are < limit.
        # We want the count of such indices in the range [i+1, N-1].
        # Let k = bisect_left(xs, limit).
        # Then robots 0 to k-1 satisfy x < limit.
        # We are interested in robots with index > i.
        # So the range of triggered robots is [i+1, k-1].
        # If i+1 > k-1, then no robots are triggered.
        # So r_i = k-1.
        # Let's check:
        # xs = [1, 3], i=0, limit=6. bisect_left([1,3], 6) -> 2. r_0 = 1. Correct.
        # xs = [1, 6], i=0, limit=6. bisect_left([1,6], 6) -> 1. r_0 = 0. Correct (no robots > 0 with x < 6).
        # So r_i = bisect_left(xs, xs[i] + d_i) - 1.
        
        k = bisect.bisect_left(xs, xs[i] + robots[i]['d'])
        r[i] = k - 1
    
    # DP
    dp = [0] * (N + 1)
    dp[N] = 1
    
    for i in range(N - 1, -1, -1):
        # Option 1: i not in set
        ways1 = dp[i+1]
        
        # Option 2: i in set
        # Must include [i+1, r[i]]
        # Remaining freedom starts from r[i] + 1
        if r[i] + 1 <= N:
            ways2 = dp[r[i] + 1]
        else:
            # r[i] + 1 > N, which means r[i] >= N. But r[i] is at most N-1.
            # So r[i] + 1 is at most N.
            # If r[i] == N-1, then r[i]+1 = N, dp[N] = 1.
            ways2 = dp[r[i] + 1]
        
        dp[i] = (ways1 + ways2) % MOD
    
    print(dp[0])

if __name__ == '__main__':
    solve()