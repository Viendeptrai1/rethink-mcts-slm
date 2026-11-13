import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        m = int(next(iterator))
        
        a = []
        for _ in range(n):
            a.append(int(next(iterator)))
            
        segments = []
        for i in range(m):
            l = int(next(iterator))
            r = int(next(iterator))
            segments.append({'id': i + 1, 'l': l, 'r': r})
            
    except StopIteration:
        return

    # If no segments, max difference is 0
    if m == 0:
        print(0)
        print(0)
        print()
        return

    # Convert 1-based indexing to 0-based for implementation
    # segments are already stored with 1-based l, r, we will adjust when processing
    
    # We need to find a subset of segments such that max(b) - min(b) is maximized.
    # b[i] = a[i] - (number of chosen segments covering index i)
    # Let k_i be the number of chosen segments covering index i.
    # b[i] = a[i] - k_i.
    # We want to maximize (max_i (a[i] - k_i)) - (min_j (a[j] - k_j)).
    # This is equivalent to finding two indices i and j (i could be j) such that:
    # (a[i] - k_i) - (a[j] - k_j) is maximized.
    # Rearranging: (a[i] - a[j]) + (k_j - k_i).
    # Here k_x depends on the choice of segments.
    
    # Approach: Iterate over all possible pairs of indices (i, j) that will be the max and min elements.
    # Since n <= 300, O(n^2) pairs is ~90,000.
    # For a fixed pair (i, j), we want to choose a subset of segments to maximize (k_j - k_i) subject to constraints?
    # Actually, k_x is determined by the count of selected segments covering x.
    # We want to maximize (a[i] - k_i) - (a[j] - k_j) = (a[i] - a[j]) + (k_j - k_i).
    # To maximize this, we need to maximize k_j and minimize k_i.
    # However, k_j and k_i are coupled because the same set of segments determines both.
    # Specifically, for any segment s, if it covers i, it contributes +1 to k_i. If it covers j, it contributes +1 to k_j.
    # If a segment covers both, it adds +1 to both, so difference k_j - k_i doesn't change.
    # If a segment covers only i, it adds +1 to k_i, so difference decreases by 1.
    # If a segment covers only j, it adds +1 to k_j, so difference increases by 1.
    # If a segment covers neither, it adds 0 to both.
    
    # So, for a fixed pair (i, j), we want to select segments such that:
    # - Segments covering ONLY j are selected (to increase k_j).
    # - Segments covering ONLY i are NOT selected (to keep k_i low).
    # - Segments covering BOTH or NEITHER don't affect the difference (k_j - k_i).
    # BUT wait, we have a constraint: we must ensure that for the resulting array b, 
    # the maximum element is indeed at i and the minimum is indeed at j?
    # No, the problem asks to maximize max(b) - min(b). If we assume i gives the max and j gives the min,
    # then we just need to maximize the value (b[i] - b[j]). Even if there's another element that becomes larger,
    # the difference might be even bigger, but that case would be covered by another pair (i', j').
    # However, strictly speaking, if we force i to be the max and j to be the min, we might miss cases where
    # the optimal solution has a different max/min pair. But since we iterate ALL pairs, we will find the optimal.
    # The only catch is: do we need to enforce that b[k] <= b[i] for all k and b[k] >= b[j] for all k?
    # Not necessarily. We just calculate the potential difference b[i] - b[j] based on our selection.
    # If the actual max-min of the resulting array is larger, say between p and q, then our iteration over (p, q)
    # will consider that pair and potentially select segments to maximize b[p] - b[q].
    # The selection strategy for a fixed (i, j) that maximizes b[i] - b[j] might accidentally make some other b[k] > b[i]
    # or b[k] < b[j], but that doesn't invalidate the fact that b[i] - b[j] is a valid difference between two elements.
    # Since we want the maximum possible value of (max - min), and max - min >= b[i] - b[j] for any specific i, j,
    # maximizing over all i, j of (b[i] - b[j]) under the assumption that we optimize b[i] - b[j] locally
    # is sufficient?
    # Let's re-evaluate.
    # We want to find a subset S of segments. Then compute D(S) = max_k(b[k]) - min_k(b[k]).
    # We want max_S D(S).
    # Let the optimal solution have max at index i* and min at index j*. Then D(S) = b[i*] - b[j*].
    # For this specific S, the value b[i*] - b[j*] is achieved.
    # In our algorithm, when we consider the pair (i*, j*), we will try to maximize b[i*] - b[j*].
    # The strategy: Select all segments that cover j* but not i*. Do NOT select any segment that covers i* but not j*.
    # What about segments covering both or neither?
    # - Segment covering both: adds 1 to k_i* and 1 to k_j*. Difference b[i*]-b[j*] unchanged.
    # - Segment covering neither: adds 0. Unchanged.
    # So, to maximize b[i*] - b[j*], we should select ALL segments that cover j* but not i*, 
    # and select NONE of the segments that cover i* but not j*.
    # What about segments covering both or neither? They don't affect b[i*] - b[j*].
    # However, could selecting extra segments (those covering both or neither) hurt the global max/min condition?
    # It might make some other b[k] larger than b[i*] or smaller than b[j*], which would only increase the global max-min.
    # But our goal is to find the max possible value. If adding extra segments increases the global range,
    # then the true max-min would be even larger, and that case would be captured by the pair corresponding to the new max/min.
    # Conversely, if adding extra segments doesn't change the max/min (i.e., i* remains max, j* remains min),
    # then the value is the same.
    # Therefore, the strategy for a fixed pair (i, j) to maximize the difference b[i] - b[j] is:
    # 1. Identify segments that cover j but not i. Select ALL of them.
    # 2. Identify segments that cover i but not j. Select NONE of them.
    # 3. Segments covering both or neither: Their contribution to b[i]-b[j] is neutral.
    #    Should we select them or not?
    #    If we select a segment covering both, b[i] decreases by 1, b[j] decreases by 1. Difference constant.
    #    If we select a segment covering neither, no change.
    #    Does selecting them affect the validity of i being max and j being min?
    #    It might. But again, if it improves the global range, a different pair will catch it.
    #    If it doesn't improve the global range (e.g., keeps i as max, j as min), then the value is the same.
    #    So, to be safe and simple, we can just pick the set that maximizes b[i]-b[j] without worrying about side effects on other indices
    #    because if side effects create a better pair, we will find it.
    #    However, there is a nuance: The problem asks for the subset that achieves the MAXIMUM possible max-min.
    #    If for pair (i,j), we construct a set S that maximizes b[i]-b[j], but the actual max-min of b(S) is actually b[p]-b[q] where p,q != i,j,
    #    and b[p]-b[q] > b[i]-b[j], then our algorithm will correctly identify b[p]-b[q] when we iterate to (p,q).
    #    Is it possible that the set S constructed for (i,j) is invalid for (p,q)?
    #    No, because for each pair we construct a candidate set. We evaluate the actual max-min of that candidate set?
    #    Wait, the problem requires us to output ONE set of segments.
    #    If we iterate all pairs, construct a set S_ij for each, compute the actual max-min of S_ij, and take the max over all pairs,
    #    is that correct?
    #    Yes. Because the optimal solution corresponds to SOME pair (i*, j*) being the max and min.
    #    Let S_opt be the optimal set. Let i* = argmax b, j* = argmin b.
    #    Then value = b[i*] - b[j*].
    #    In our iteration for (i*, j*), we construct S_candidate.
    #    S_candidate includes all segments covering j* but not i*.
    #    Does S_candidate produce a value >= b[i*] - b[j*] (from S_opt)?
    #    In S_opt, let k_x be count for index x.
    #    b[i*] - b[j*] = (a[i*] - k_i*) - (a[j*] - k_j*) = (a[i*] - a[j*]) + (k_j* - k_i*).
    #    In S_candidate, we select more segments than S_opt potentially?
    #    S_opt might not include all segments covering j* but not i*.
    #    If we add such a segment to S_opt, k_j* increases by 1, k_i* unchanged (since it doesn't cover i*).
    #    So b[i*] - b[j*] increases by 1.
    #    So S_candidate definitely yields a b[i*] - b[j*] >= that of S_opt.
    #    Let the resulting array be b'. Then max(b') - min(b') >= b'[i*] - b'[j*] >= b[i*] - b[j*] (optimal).
    #    Since optimal is the maximum possible, S_candidate must also be optimal (or better, which implies optimal was not truly optimal).
    #    Thus, for each pair (i, j), the strategy "Select all segments covering j but not i" gives a valid candidate.
    #    We compute the actual max-min for this candidate and update the global maximum.
    
    # Implementation details:
    # n, m <= 300. O(n^2 * m) = 90000 * 300 = 27,000,000 operations. This is acceptable for 1-2 seconds in PyPy.
    
    best_diff = -1
    best_set = []
    
    # Precompute coverage to speed up? Or just iterate.
    # Given constraints, simple iteration is fine.
    
    # Convert segments to 0-based l, r
    for seg in segments:
        seg['l'] -= 1
        seg['r'] -= 1

    # Iterate over all pairs (i, j)
    # i is the index that should be the MAX
    # j is the index that should be the MIN
    for i in range(n):
        for j in range(n):
            # Construct the set of segments
            # Rule: Select segment if it covers j but does NOT cover i.
            current_set = []
            for idx, seg in enumerate(segments):
                # Check if covers j
                covers_j = (seg['l'] <= j <= seg['r'])
                # Check if covers i
                covers_i = (seg['l'] <= i <= seg['r'])
                
                if covers_j and not covers_i:
                    current_set.append(idx + 1) # 1-based index
            
            # Calculate the array b and find max - min
            # b[k] = a[k] - count of segments in current_set covering k
            # To do this efficiently:
            # We can iterate over all k and count coverage.
            
            # Optimization: Since we only changed specific segments, maybe incremental?
            # No, O(m) per pair is fine.
            
            # Build b
            # Initialize counts
            # Since m is small, we can just iterate segments for each k? That's O(n*m).
            # Total O(n^2 * n * m) = 300^4 is too big (8.1e9).
            # We need O(n^2 * m) or O(n^2).
            # Current approach: For each pair, iterate all segments to build b?
            # Building b takes O(n * m) naively.
            # Total O(n^2 * n * m) is bad.
            
            # Better approach:
            # For a fixed pair (i, j), the set of segments is fixed.
            # We can compute the effect on the array.
            # The segments we select are those in S_sel.
            # We need max_k (a[k] - count(k)) - min_k (a[k] - count(k)).
            # count(k) = sum(1 for s in S_sel if s covers k).
            # We can compute count array in O(m) by iterating segments and updating an array.
            # Then scan array in O(n).
            # Total per pair: O(m + n).
            # Total overall: O(n^2 * (m + n)).
            # 300^2 * 600 = 90000 * 600 = 54,000,000.
            # This is acceptable.
            
            # Let's implement this.
            
            # Create a difference array or just a count array
            counts = [0] * n
            for idx, seg in enumerate(current_set):
                # Retrieve segment details (we stored them in 'segments' list, but current_set has indices)
                # segments is list of dicts.
                s = segments[seg - 1]
                # Apply decrement
                # But wait, applying decrement directly to a copy of a is easier.
                # Actually, we can just iterate segments in current_set and mark.
                # Since m is small, iterating is fine.
                pass
            
            # More efficient construction:
            # Instead of building counts by iterating segments for each k, 
            # iterate segments in current_set and increment counts in range.
            # Using a difference array for range updates would be O(m) to build and O(n) to scan.
            # But since m is small, direct update is O(m * length) which is O(m*n) worst case per pair?
            # No, if we iterate segments and for each segment iterate the range, it's O(m*n) per pair.
            # That leads to O(n^2 * m * n) = O(n^3 * m). Bad.
            
            # Use difference array (or sweep line) to compute counts in O(m + n).
            diff = [0] * (n + 1)
            for idx, seg in enumerate(current_set):
                s = segments[seg - 1]
                diff[s['l']] -= 1
                diff[s['r'] + 1] += 1
            
            # Compute prefix sums to get counts
            current_k = 0
            max_b = -float('inf')
            min_b = float('inf')
            
            # We can compute max and min on the fly
            for k in range(n):
                current_k += diff[k]
                val = a[k] - current_k
                if val > max_b:
                    max_b = val
                if val < min_b:
                    min_b = val
            
            diff_val = max_b - min_b
            if diff_val > best_diff:
                best_diff = diff_val
                best_set = current_set.copy()
            elif diff_val == best_diff and len(best_set) > 0: # Tie breaking? Any is fine.
                pass

    print(best_diff)
    print(len(best_set))
    print(*(best_set))

if __name__ == '__main__':
    solve()