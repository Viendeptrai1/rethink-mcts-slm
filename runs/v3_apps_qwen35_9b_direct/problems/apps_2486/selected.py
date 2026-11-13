import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    A = []
    for i in range(N):
        A.append(int(data[2 + i]))
    
    # Sort A to help with logic, but we need to track original indices if needed.
    # However, the problem asks for the count, so we can work on a sorted copy.
    # But wait: the definition of "good subset" and "unnecessary" depends on the values.
    # The specific index doesn't matter for the count, only the values do.
    # Let's sort A to process efficiently.
    sorted_A = sorted(A)
    
    # We need to determine for each card (in the original set, but since all cards with same value are indistinguishable in terms of logic, 
    # and we just need the count, we can process the sorted array and map back or just count).
    # Actually, the condition is:
    # Card i is unnecessary if for ANY good subset S containing i, (S \ {i}) is also good.
    # This is equivalent to: There is NO good subset S containing i such that sum(S) >= K and sum(S) - a_i < K.
    # In other words, card i is NOT unnecessary if there exists a subset S containing i such that:
    # sum(S) >= K AND sum(S) - a_i < K.
    # This implies sum(S) is in [K, K + a_i - 1].
    # So, card i is NOT unnecessary if we can form a sum S' (using other cards) such that:
    # K <= S' + a_i < K + a_i
    # => K - a_i <= S' < K
    # Since S' must be a sum of a subset of OTHER cards, we need to check if there exists a subset sum S' in [max(0, K - a_i), K - 1].
    
    # If such an S' exists, then card i is NOT unnecessary.
    # If no such S' exists, then card i is unnecessary.
    
    # So the algorithm is:
    # 1. Compute all possible subset sums of the other cards for each card i.
    #    Since N is up to 5000, we cannot do O(N * 2^N).
    #    However, K is small (<= 5000). We only care about subset sums up to K-1.
    #    Any sum >= K is not useful for the condition "sum(S') < K".
    #    So we can use a bitset (or boolean array) to track reachable sums up to K-1.
    
    # But we need to do this for EACH card i. Doing it naively for each card would be O(N * K), which is 5000*5000 = 25e6, feasible.
    # Wait, if we remove card i, we need the subset sums of the remaining N-1 cards.
    # We can precompute the subset sums of ALL cards up to K-1.
    # Let dp[s] be true if sum s is achievable using some subset of cards.
    # But if we remove card i, we need to know if s is achievable WITHOUT card i.
    # This is a classic "subset sum with exclusion" problem.
    # We can use prefix and suffix DP arrays.
    # Let pre[i][s] be true if sum s is achievable using cards 0..i-1.
    # Let suf[i][s] be true if sum s is achievable using cards i..N-1.
    # Then for card i, the achievable sums using other cards are those s where pre[i][s] OR suf[i+1][s] is true.
    # Actually, we can combine them: a sum s is achievable without card i if it is achievable using a subset of {0..i-1} OR {i+1..N-1}.
    # So we need to check if there exists s in [max(0, K - a_i), K - 1] such that (pre[i][s] or suf[i+1][s]) is true.
    
    # Constraints: N, K <= 5000.
    # Precomputing pre[i][s] for all i and s up to K-1:
    # Size: N * K = 25e6 booleans. In Python, a list of lists might be heavy on memory and time.
    # 25e6 integers/bools is about 25MB-100MB, which is fine.
    # Time to compute: O(N*K). 25e6 operations is fine for 2 seconds in Python if optimized (using bitsets or efficient loops).
    # However, pure Python loops for 25e6 might be slow (could take 5-10 seconds).
    # We need to optimize.
    
    # Optimization: Use integers as bitmasks.
    # pre[i] will be an integer where the j-th bit is 1 if sum j is achievable.
    # suf[i] similarly.
    # Then pre[i] can be computed from pre[i-1] by: pre[i] = pre[i-1] | (pre[i-1] << a[i-1])
    # But we only need bits up to K-1.
    # Shifting a large integer and masking is efficient in Python.
    
    # Steps:
    # 1. Create pre array of size N+1. pre[0] = 1 (sum 0 is achievable).
    #    pre[i] represents sums achievable using first i cards (indices 0 to i-1).
    #    We only care about bits 0 to K-1.
    #    So after each shift, we can mask with ((1 << K) - 1).
    # 2. Create suf array of size N+1. suf[N] = 1.
    #    suf[i] represents sums achievable using cards from index i to N-1.
    #    suf[i] = suf[i+1] | (suf[i+1] << a[i])
    #    Again, mask with ((1 << K) - 1).
    # 3. For each card i (0-indexed in sorted array, but values matter):
    #    val = A[i]
    #    We need to check if there is any bit set in (pre[i] | suf[i+1]) in the range [K - val, K - 1].
    #    Let combined = pre[i] | suf[i+1]
    #    We need to check if (combined >> (K - val)) & ((1 << val) - 1) is non-zero.
    #    Wait, the range is [K - val, K - 1].
    #    If K - val < 0, then the range starts at 0. So effective start is max(0, K - val).
    #    Let start = max(0, K - val)
    #    Let end = K - 1
    #    If start > end, then no such sum exists -> card is unnecessary.
    #    Otherwise, we check bits from start to end.
    #    We can extract these bits: mask = ((1 << (end - start + 1)) - 1) << start
    #    If (combined & mask) != 0, then such a sum exists -> card is NOT unnecessary.
    #    Else, card is unnecessary.
    
    # Complexity:
    # Precomputation: N steps, each step involves bitwise shift and OR on integers of size K bits.
    # Python handles large integers efficiently. Shifting a K-bit integer is O(K/word_size).
    # Total time: O(N * K / 64). With N=5000, K=5000, operations ~ 5000 * 80 ~ 400k word ops. Very fast.
    # Query: N queries, each O(1) bitwise ops.
    # Total time is well within limits.
    
    # Note: The problem statement says "For each card i". The input order matters for the output count?
    # No, the output is just the number of unnecessary cards. The cards are indistinguishable except for their values.
    # Sorting A does not change the set of values, so the count of unnecessary cards remains the same.
    # Example: A = [1, 4, 3]. Sorted: [1, 3, 4].
    # Card with value 1: check sums in [6-1, 5] = [5, 5].
    # Card with value 4: check sums in [6-4, 5] = [2, 5].
    # Card with value 3: check sums in [6-3, 5] = [3, 5].
    # The logic holds regardless of order.
    
    # Implementation details:
    # Mask for K bits: limit = (1 << K) - 1
    # But we only need up to K-1. So mask = (1 << K) - 1 covers 0 to K-1.
    
    limit = (1 << K) - 1
    
    # Precompute prefix sums
    pre = [0] * (N + 1)
    pre[0] = 1
    for i in range(N):
        # pre[i+1] = pre[i] | (pre[i] << A[i])
        # We can apply mask to keep size manageable, though Python handles large ints automatically.
        # Applying mask might speed up slightly by keeping bit length small.
        val = A[i]
        pre[i+1] = (pre[i] | (pre[i] << val)) & limit
        
    # Precompute suffix sums
    suf = [0] * (N + 1)
    suf[N] = 1
    for i in range(N - 1, -1, -1):
        val = A[i]
        suf[i] = (suf[i+1] | (suf[i+1] << val)) & limit
        
    unnecessary_count = 0
    for i in range(N):
        val = A[i]
        # We need to check if there is a sum s in [max(0, K - val), K - 1] achievable without card i.
        # Achievable without card i means achievable using cards 0..i-1 OR cards i+1..N-1.
        # This corresponds to bits set in pre[i] OR suf[i+1].
        
        start = K - val
        if start < 0:
            start = 0
        end = K - 1
        
        if start > end:
            # No sum in range [K-val, K-1] exists because K-val >= K (since val <= 0, but val >= 1)
            # Actually if val >= K, then K-val <= 0. So start=0. end=K-1. Range is valid.
            # If val < K, then K-val > 0.
            # The only case start > end is if K - val > K - 1 => -val > -1 => val < 1.
            # But constraints say a_i >= 1. So start <= end always?
            # Wait: if K=1, val=1. start = 0, end = 0. Range [0,0].
            # If K=1, val=100. start = 1-100 = -99 -> 0. end = 0. Range [0,0].
            # So start > end is impossible given a_i >= 1 and K >= 1?
            # Let's recheck: start = max(0, K-val). end = K-1.
            # If K-val > K-1 => -val > -1 => val < 1. Impossible.
            # So start <= end always.
            pass
        
        combined = pre[i] | suf[i+1]
        
        # Check if any bit from start to end is set.
        # We can create a mask for bits [start, end].
        # Number of bits = end - start + 1
        # Mask = ((1 << (end - start + 1)) - 1) << start
        # But if end - start + 1 is large, this is fine.
        
        num_bits = end - start + 1
        mask = ((1 << num_bits) - 1) << start
        
        if (combined & mask) == 0:
            unnecessary_count += 1
            
    print(unnecessary_count)

if __name__ == '__main__':
    solve()