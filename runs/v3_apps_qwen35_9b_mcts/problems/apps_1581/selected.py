import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    K = int(input_data[1])
    MOD = 10**9 + 7

    # Precompute valid next values for each x in [1, N]
    # valid_next[x] = list of y in [1, N] such that x * y <= N
    # Since we only need the count of such y, we can compute counts directly.
    # However, the transition depends on the specific value of x for the next step.
    # So we need the list of valid next values.
    # But storing lists for all N up to 10^9 is impossible.
    # Observation: The number of distinct values of x that appear in a sequence is limited?
    # No, x can be any value from 1 to N.
    # However, note that if x > sqrt(N), then y must be <= N/x < sqrt(N).
    # Also, if x <= sqrt(N), then y can be up to N/x.
    # We can split the state space.
    # Let S = floor(sqrt(N)).
    # For x <= S, the next value y can be any integer in [1, floor(N/x)].
    # For x > S, the next value y must be in [1, floor(N/x)] which is a subset of [1, S].
    # So we can define two types of states:
    # Type 1: x in [1, S]
    # Type 2: x in [S+1, N]
    # But Type 2 states are many (N - S). We cannot have a DP array of size N.
    # However, notice that for x > S, the set of valid next values is [1, floor(N/x)].
    # The value floor(N/x) is constant for ranges of x.
    # But the DP state needs to track the exact value of the last element because the constraint for the next step depends on it.
    # Wait, the problem asks for sequences of length K.
    # Let dp[i][x] be the number of sequences of length i ending with x.
    # dp[i][x] = sum(dp[i-1][y] for y such that y*x <= N)
    # This is equivalent to: dp[i][x] = sum(dp[i-1][y] for y in [1, floor(N/x)])
    # Let P[i][v] = sum_{j=1}^{v} dp[i][j] (prefix sums of dp[i]).
    # Then dp[i][x] = P[i-1][floor(N/x)].
    # We can compute dp[i] from dp[i-1] using prefix sums.
    # The values of x range from 1 to N. We cannot iterate up to N if N is 10^9.
    # However, note that floor(N/x) takes at most 2*sqrt(N) distinct values.
    # Also, the values of x that matter are those where floor(N/x) changes, or simply we can group x by the value of floor(N/x).
    # But wait, the recurrence is: dp[i][x] = P[i-1][floor(N/x)].
    # This means dp[i][x] is constant for all x in a range where floor(N/x) is constant.
    # Let v = floor(N/x). Then x is in (N/(v+1), N/v].
    # So we can group x by the value v = floor(N/x).
    # There are at most 2*sqrt(N) such groups.
    # Let's denote the groups by the value v = floor(N/x).
    # For a fixed v, the range of x is L_v = floor(N/(v+1)) + 1 to R_v = floor(N/v).
    # For all x in [L_v, R_v], dp[i][x] = P[i-1][v].
    # So we can maintain the DP state as a list of (v, count) pairs?
    # Actually, we need the prefix sums P[i-1] to compute P[i].
    # P[i][v] = sum_{x=1}^{v} dp[i][x].
    # But dp[i][x] is defined for x up to N.
    # However, note that if x > N, it's not possible (since elements are positive integers and product <= N, so each element <= N).
    # Also, for x > N, dp[i][x] = 0.
    # So we only care about x in [1, N].
    # The key is that dp[i][x] is constant on intervals where floor(N/x) is constant.
    # Let's represent the DP state at step i as a list of segments.
    # Each segment is (start_x, end_x, value), meaning for x in [start_x, end_x], dp[i][x] = value.
    # The number of such segments is O(sqrt(N)).
    # How to compute the next state?
    # We need P[i-1][v] for various v.
    # P[i-1][v] = sum_{x=1}^{v} dp[i-1][x].
    # Since dp[i-1] is piecewise constant, we can compute P[i-1][v] for any v by summing the values of the segments that are fully or partially covered by [1, v].
    # Then, for the next state dp[i][x], we set it to P[i-1][floor(N/x)].
    # This means dp[i][x] is constant for x in the range where floor(N/x) is constant.
    # So the new state will also be piecewise constant with O(sqrt(N)) segments.
    # Algorithm:
    # 1. Initialize dp state for i=1: dp[1][x] = 1 for all x in [1, N].
    #    This can be represented as one segment: (1, N, 1).
    # 2. For step from 1 to K-1:
    #    a. Compute the prefix sum function P[v] = sum_{x=1}^{v} dp[x] for the current state.
    #       Since the current state is a list of segments, we can compute P[v] for any v in O(number of segments).
    #       But we need P[v] for v = floor(N/x) for all x.
    #       Actually, we only need P[v] for v that appear as floor(N/x) for some x.
    #       These v are exactly the values floor(N/x) for x in [1, N].
    #       There are O(sqrt(N)) such values.
    #       Let's collect all unique values of v = floor(N/x) for x in [1, N].
    #       We can generate these values by iterating x from 1 to sqrt(N) and also considering the symmetric part.
    #       Actually, the standard way to iterate over values of floor(N/x) is:
    #         l = 1
    #         while l <= N:
    #             v = N // l
    #             r = N // v
    #             # for x in [l, r], floor(N/x) = v
    #             l = r + 1
    #       This gives us the intervals for x and the corresponding v.
    #    b. For each interval [l, r] of x (where floor(N/x) = v), the new value for dp[i][x] is P[v].
    #       So we form a new segment (l, r, P[v]).
    #    c. Update the current state to this new list of segments.
    # 3. After K-1 steps, we have dp[K][x] for x in [1, N].
    #    The answer is sum_{x=1}^{N} dp[K][x].
    #    This can be computed by summing (end_x - start_x + 1) * value for each segment.

    # Implementation details:
    # Represent state as a list of tuples (l, r, val).
    # Initially: [(1, N, 1)]
    # In each step:
    #   Generate the intervals for x: [l, r] such that floor(N/x) = v.
    #   For each such interval, we need P[v] = sum_{x=1}^{v} dp[x].
    #   To compute P[v] efficiently:
    #     We have the current state as a list of segments.
    #     We can compute the total sum up to v by iterating through the segments.
    #     Since the number of segments is O(sqrt(N)), and we do this for each interval (also O(sqrt(N))), the total complexity per step is O((sqrt(N))^2) = O(N).
    #     Wait, O(N) per step with K steps would be O(N*K) which is too slow (10^9 * 100).
    #     We need a faster way to compute P[v].
    #     Notice that the segments are sorted by l.
    #     We can precompute the prefix sums of the segment values (weighted by length) to quickly compute P[v].
    #     Let the segments be S_1, S_2, ..., S_m.
    #     Let total_len_j = r_j - l_j + 1.
    #     Let val_j = value of S_j.
    #     Let cum_len_j = sum_{k=1}^{j} total_len_k.
    #     Let cum_val_j = sum_{k=1}^{j} (total_len_k * val_k).
    #     Then for a given v, we can find the segment j such that l_j <= v <= r_j.
    #     Then P[v] = cum_val_{j-1} + (v - l_j + 1) * val_j.
    #     We can use binary search (bisect) to find j in O(log m).
    #     Total complexity per step: O(m * log m) where m = O(sqrt(N)).
    #     So total complexity: O(K * sqrt(N) * log(sqrt(N))) which is acceptable.

    # Steps refined:
    # 1. Represent state as list of (l, r, val).
    # 2. Precompute cumulative lengths and cumulative values for the current state to allow O(log m) query of P[v].
    # 3. Generate the intervals for x (where floor(N/x) is constant).
    # 4. For each interval [l, r] with v = floor(N/x), compute P[v] using the precomputed arrays.
    # 5. Create new segments for the next state.
    # 6. Repeat K-1 times.
    # 7. Sum up the final state.

    # Edge case: N=1.
    # If N=1, then only sequence is (1,1,...,1). Answer 1.
    # Our logic should handle it.

    # Let's code.

    # Initial state: x in [1, N], dp[x] = 1.
    # But note: if N is large, we cannot create an array of size N.
    # We use the segment representation.
    # Initial segments: [(1, N, 1)]

    # However, note that for the first step (i=1), we are counting sequences of length 1.
    # The problem asks for sequences of length K.
    # The recurrence: dp[i][x] = sum_{y: y*x<=N} dp[i-1][y] = P[i-1][floor(N/x)].
    # This recurrence holds for i >= 2.
    # For i=1, dp[1][x] = 1 for all x in [1, N].
    # So we start with state for i=1, and iterate K-1 times to get state for i=K.

    # Special case: K=1.
    # Then the answer is N.
    # Our loop runs 0 times, so we just sum the initial state.

    # Let's implement.

    # Precompute the intervals for x for the entire process?
    # The intervals for x (where floor(N/x) is constant) are fixed for a given N.
    # We can precompute them once.
    # Let intervals_x be a list of (l, r, v) where for x in [l, r], floor(N/x) = v.
    # We can generate this list once.

    intervals_x = []
    l = 1
    while l <= N:
        v = N // l
        if v == 0:
            # This should not happen since l <= N
            r = N
        else:
            r = N // v
        intervals_x.append((l, r, v))
        l = r + 1

    # Now, represent the current DP state as a list of segments: (l, r, val)
    # Initially for i=1: [(1, N, 1)]
    current_segments = [(1, N, 1)]

    # Precompute cumulative data for the initial state?
    # We will recompute cumulative data at the beginning of each step.

    for step in range(1, K):
        # Step: compute next state from current state
        # 1. Precompute cumulative lengths and values for current_segments
        #    segments: (l, r, val)
        #    We need to answer: given v, what is sum_{x=1}^{v} dp[x]?
        #    We can do this by finding the segment that contains v, or the last segment before v.
        
        # Build cumulative arrays
        cum_len = []
        cum_val = []
        current_l = 1
        current_cum_len = 0
        current_cum_val = 0
        
        # We also need to quickly find the segment containing a given v.
        # Since segments are sorted by l, we can use bisect on the l's.
        seg_l = [seg[0] for seg in current_segments]
        
        for seg in current_segments:
            l_seg, r_seg, val_seg = seg
            length = r_seg - l_seg + 1
            current_cum_len += length
            current_cum_val = (current_cum_val + length * val_seg) % MOD
            cum_len.append(current_cum_len)
            cum_val.append(current_cum_val)
        
        # 2. Generate next segments
        next_segments = []
        
        for (l_x, r_x, v) in intervals_x:
            # For x in [l_x, r_x], floor(N/x) = v.
            # So dp[next][x] = P[v] = sum_{y=1}^{v} dp[y]
            # Compute P[v]
            # Find the segment in current_segments that contains v.
            # We can use bisect_right on seg_l to find the index of the first segment with l > v.
            # Then the segment before that index is the one containing v (if any).
            # If v < current_segments[0].l, then P[v] = 0.
            # But v = floor(N/x) and x >= 1, so v <= N.
            # Also, the segments cover [1, N].
            # So v is always in [1, N].
            
            import bisect
            idx = bisect.bisect_right(seg_l, v)
            # idx is the number of segments with l <= v.
            # The segment containing v is at index idx-1.
            if idx == 0:
                P_v = 0
            else:
                # The segment at idx-1 is (l_seg, r_seg, val_seg)
                l_seg = current_segments[idx-1][0]
                r_seg = current_segments[idx-1][1]
                val_seg = current_segments[idx-1][2]
                
                # Sum of full segments before idx-1
                if idx > 1:
                    prev_cum_val = cum_val[idx-2]
                else:
                    prev_cum_val = 0
                
                # Partial segment
                # The segment covers [l_seg, r_seg]. We need sum from l_seg to v.
                # Number of terms = v - l_seg + 1
                count = v - l_seg + 1
                P_v = (prev_cum_val + count * val_seg) % MOD
            
            # Now, for x in [l_x, r_x], the value is P_v.
            # But note: we must ensure that the range [l_x, r_x] is within [1, N].
            # It is, by construction.
            # Also, we must ensure that we don't create overlapping segments or gaps.
            # The intervals_x are disjoint and cover [1, N].
            # So we can just append (l_x, r_x, P_v) to next_segments.
            next_segments.append((l_x, r_x, P_v))
        
        current_segments = next_segments

    # Finally, sum up the values in the last state
    total = 0
    for (l, r, val) in current_segments:
        count = (r - l + 1) % MOD
        total = (total + count * val) % MOD

    print(total)

if __name__ == '__main__':
    solve()