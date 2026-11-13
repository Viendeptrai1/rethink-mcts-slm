import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    K = int(input_data[1])
    MOD = 1_000_000_007

    if K == 1:
        print(N % MOD)
        return

    # Find all x such that x * y <= N for some y >= 1
    # This is equivalent to x <= N (since min y is 1)
    # But we need the count of pairs (a, b) such that a*b <= N
    # For dynamic programming, we need cnt[v] = number of x such that x * v <= N
    # i.e., x <= floor(N / v)
    # So cnt[v] = N // v

    # However, K is small (<= 100), but N is large (<= 10^9).
    # We cannot create an array of size N.
    # We need to group values of v that have the same value of N // v.
    # This is a standard technique using square root decomposition.

    # Let's define a function to get the list of (value, count) pairs for N // v
    # where v ranges from 1 to N.
    # Actually, in our DP, the state will be the value of the last element.
    # dp[i][v] = number of sequences of length i ending with value v.
    # Transition: dp[i][v] = sum(dp[i-1][u]) for all u such that u * v <= N
    #                = sum(dp[i-1][u]) for u in [1, floor(N/v)]
    #
    # Notice that the transition only depends on the prefix sum of dp[i-1].
    # Let S[i-1][x] = sum(dp[i-1][1..x]).
    # Then dp[i][v] = S[i-1][floor(N/v)].
    #
    # The values of floor(N/v) are constant over ranges. We can use this to speed up.
    # However, since K is small, maybe we can just compute the distinct values of v that matter?
    # Actually, the "next" values we need are floor(N/v) for v in the support of the current dp.
    # Initially, for K=1, dp[1][v] = 1 for all v in [1, N].
    # So the support is [1, N].
    # Then for K=2, dp[2][v] = N // v.
    # The values of v where dp[2][v] changes are the divisors of N? No, floor(N/v) changes at sqrt(N) points.
    #
    # Alternate approach:
    # Instead of tracking every integer v, track the groups of v that have the same "transition behavior".
    # But the transition for a specific v depends on N//v.
    # Let's reframe:
    # We want to compute the number of sequences of length K.
    # Let f(i, v) be the number of sequences of length i ending with v.
    # f(i, v) = sum_{u=1}^{floor(N/v)} f(i-1, u)
    #
    # Notice that f(i, v) is constant for v in ranges where floor(N/v) is constant.
    # Let's denote g(i, x) = sum_{v: floor(N/v) = x} f(i, v). This might be complicated.
    #
    # Better approach using the property of floor(N/v):
    # The values of floor(N/v) take at most 2*sqrt(N) distinct values.
    # However, N is up to 10^9, so 2*sqrt(N) is about 63245, which is manageable for K=100?
    # 63245 * 100 is 6e6 operations, which is acceptable in Python if implemented carefully.
    #
    # Let's try to maintain the DP state as a list of (value_start, value_end, count) tuples?
    # Or simply a dictionary mapping value -> count? But the values are contiguous ranges with constant count.
    # So we can represent the dp array as a list of (l, r, c) meaning for v in [l, r], dp[v] = c.
    #
    # Initial state (K=1):
    # One range: [1, N] with count 1.
    #
    # Transition from step i-1 to i:
    # We have a list of ranges R_prev = [(l1, r1, c1), (l2, r2, c2), ...]
    # For a new v, dp[i][v] = sum of dp[i-1][u] for u in [1, floor(N/v)].
    # Since dp[i-1] is piecewise constant, the sum is a linear function of the endpoint of the prefix?
    # No, the sum is constant if the prefix [1, X] covers a set of full ranges and part of a range.
    #
    # Let's define a function prefix_sum_prev(X) that returns sum_{u=1}^{X} dp[i-1][u].
    # Since dp[i-1] is represented by ranges, we can compute this in O(number_of_ranges).
    # Then for each range [L, R] in the next step, for any v in [L, R], floor(N/v) is constant, say X.
    # Then dp[i][v] = prefix_sum_prev(X).
    # So the new dp[i][v] is also constant over [L, R]!
    #
    # Algorithm:
    # 1. Represent current dp as a list of (l, r, count). Initially [(1, N, 1)].
    # 2. For step from 1 to K-1:
    #    a. Create a new list for next dp.
    #    b. First, identify the ranges of v where floor(N/v) is constant.
    #       These are the "harmonic" ranges. Let's call this list harmonic_ranges.
    #       harmonic_ranges will be [(L1, R1), (L2, R2), ...] covering [1, N].
    #       For each (L, R) in harmonic_ranges, X = N // L (which equals N // v for all v in [L, R]).
    #    c. For each harmonic range (L, R) with X = N // L:
    #       Calculate S = prefix_sum_prev(X). This is sum of dp[i-1][u] for u=1..X.
    #       Then for all v in [L, R], dp[i][v] = S.
    #       We can merge adjacent ranges in the new dp if they have the same count.
    #
    # Optimization:
    # The number of harmonic ranges is O(sqrt(N)). Let M = number of harmonic ranges.
    # M <= 2*sqrt(N) ~ 63245.
    # In each step, we iterate M times. Total complexity O(K * sqrt(N)).
    # With K=100, N=10^9, operations ~ 6.3e6. In Python, this might be tight but likely passable (1-2 sec limit usually allows ~10^7-10^8 ops in C++, Python is slower, but simple arithmetic loops might pass).
    #
    # Let's refine the prefix_sum_prev calculation.
    # We have prev_dp as list of (l, r, count).
    # To compute prefix_sum_prev(X):
    #   Iterate through prev_dp ranges, accumulating count * length, until r >= X.
    #   If we land in the middle of a range, add (X - l + 1) * count and stop.
    #   This is O(M_prev).
    #
    # So total per step: O(M_harmonic + M_prev). Since M_prev <= M_harmonic, it's O(M).
    # Total time O(K * sqrt(N)).
    #
    # Let's implement this.

    def get_harmonic_ranges(n):
        """Returns list of (l, r) such that for v in [l, r], n//v is constant."""
        ranges = []
        l = 1
        while l <= n:
            val = n // l
            if val == 0:
                r = n
            else:
                # The largest r such that n // r == val is r = n // val
                r = n // val
                if r > n:
                    r = n
            ranges.append((l, r))
            l = r + 1
        return ranges

    # Current DP state: list of (l, r, count)
    # Initially for K=1, dp[v] = 1 for all v in [1, N]
    current_dp = [(1, N, 1)]

    # Precompute harmonic ranges for N (they are constant throughout)
    harmonic = get_harmonic_ranges(N)
    # Convert to sets or keep as list of tuples. List is fine.
    # Also precompute the value X = N // l for each harmonic range to avoid division in loop.
    harmonic_X = [harmonic[i][0] for i in range(len(harmonic))] # Actually N//l is constant in the range, so just take first element

    MOD = 1_000_000_007

    # Function to compute prefix sum of current_dp up to X
    def get_prefix_sum(X):
        total = 0
        for l, r, count in current_dp:
            if r <= X:
                total = (total + count * (r - l + 1)) % MOD
            else:
                # Overlaps X
                overlap = X - l + 1
                total = (total + count * overlap) % MOD
                break
        return total

    # Iterate K-1 times to extend the sequence
    for _ in range(K - 1):
        new_dp = []
        # For each harmonic range [L, R], the value X = N // L is constant.
        # dp_new[v] = get_prefix_sum(X) for all v in [L, R].
        # We collect these and merge if consecutive ranges have same count.
        
        last_l, last_r, last_count = -1, -1, -1
        
        for l, r in harmonic:
            if l > N:
                break
            X = N // l
            s = get_prefix_sum(X)
            
            if s == 0:
                # If sum is 0, then all subsequent ranges will also have sum 0? 
                # Not necessarily, but if s=0, then no sequences can extend.
                # However, since we start with positive counts, and X decreases, eventually sum becomes 0.
                # Once sum is 0, all further v will have dp[v]=0.
                # We can stop early? 
                # But we need to represent the full range [1, N] with 0s if we want to be consistent,
                # or just not add them. Since we only care about non-zero counts eventually, 
                # we can skip adding ranges with 0 count.
                # However, the harmonic ranges cover [1, N]. If we skip, the next step's prefix sum might be wrong if we assume coverage?
                # No, prefix sum iterates over current_dp ranges. If we don't store 0 ranges, get_prefix_sum just stops when it runs out of ranges.
                # That is correct.
                continue

            if last_l != -1:
                if last_count == s:
                    # Merge with previous
                    last_r = r
                else:
                    # Push previous
                    new_dp.append((last_l, last_r, last_count))
                    last_l, last_r, last_count = l, r, s
            else:
                last_l, last_r, last_count = l, r, s

        if last_l != -1:
            new_dp.append((last_l, last_r, last_count))
        
        current_dp = new_dp

    # The answer is the sum of all counts in current_dp
    ans = 0
    for l, r, count in current_dp:
        ans = (ans + count * (r - l + 1)) % MOD

    print(ans)

solve()