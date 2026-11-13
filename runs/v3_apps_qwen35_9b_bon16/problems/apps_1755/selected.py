import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)

    n = int(next(iterator))
    k = int(next(iterator))

    a = [0] * (n + 1)
    for i in range(1, n + 1):
        a[i] = int(next(iterator))

    b_set = set()
    if k > 0:
        for _ in range(k):
            b_set.add(int(next(iterator)))

    # We need to fill the gaps between segments of fixed indices with strictly increasing integers.
    # Let's define segments of indices that are NOT in b.
    # Within each segment, we can change values arbitrarily.
    # Between two segments (or before the first, after the last), we have fixed constraints.
    
    # Collect all fixed indices and their values
    # We will process the array in blocks separated by fixed indices.
    
    # First, let's identify the segments of "changeable" indices.
    # A segment is a contiguous range [L, R] of indices where none are in b.
    # The values at indices in b are fixed and must be respected.
    
    # Let's create a list of events: (index, value) for all i in b.
    # Also, we need to consider the constraints imposed by the gaps.
    
    # Strategy:
    # 1. Identify all fixed positions (indices in b). Let these be p_1, p_2, ..., p_k.
    # 2. The array is divided into segments:
    #    - Before p_1: indices [1, p_1 - 1]
    #    - Between p_i and p_{i+1}: indices [p_i + 1, p_{i+1} - 1]
    #    - After p_k: indices [p_k + 1, n]
    # 3. For each segment, we need to assign values such that:
    #    - If the segment is before p_1: a[1] > ... > a[p_1 - 1] < a[p_1]
    #    - If the segment is between p_i and p_{i+1}: a[p_i] < ... < a[p_i + 1] < ... < a[p_{i+1} - 1] < a[p_{i+1}]
    #    - If the segment is after p_k: a[p_k] < ... < a[n]
    #
    # 4. We check if the fixed values themselves form a strictly increasing sequence. If not, impossible.
    # 5. For each segment, we calculate the minimum operations needed.
    #    Actually, within a segment of length L, if we can fill it perfectly with arithmetic progression or just increasing sequence,
    #    we might need 0 operations if the existing values already form a valid increasing subsequence that fits the bounds.
    #    Wait, the problem asks for MINIMUM operations.
    #    We can change ANY value in the non-b indices.
    #    So for a segment [L, R], we want to keep as many original values as possible such that:
    #    - They are strictly increasing.
    #    - They fit between the boundary values (if any).
    #
    # This is equivalent to: For a segment [L, R] with boundaries (prev_val, next_val),
    # find the Longest Increasing Subsequence (LIS) of the existing values in a[L...R]
    # BUT with the constraint that the chosen subsequence must fit in the range (prev_val, next_val) with step at least 1.
    # Actually, since we can pick ANY integers for the modified positions, the only constraint is:
    # If we keep a subset of indices i_1, i_2, ..., i_m in [L, R] with original values v_1, v_2, ..., v_m,
    # then we must have:
    #   prev_val < v_1 < v_2 < ... < v_m < next_val
    # And for any two kept indices i_x and i_y (with x < y), we must have a[i_x] < a[i_y].
    # Additionally, the gaps between kept values must be fillable.
    # Since we can pick any integers, as long as a[i_x] < a[i_y], we can always fill the intermediate indices
    # with values strictly between a[i_x] and a[i_y] (e.g., a[i_x]+1, a[i_x]+2, ...).
    # The only hard constraint is the boundaries.
    # So the condition simplifies to:
    # Find the longest subsequence of indices in [L, R] such that:
    #   val(L-1) < a[i_1] < a[i_2] < ... < a[i_m] < val(R+1)
    # where val(L-1) is the fixed value at L-1 (or -infinity if L=1),
    # and val(R+1) is the fixed value at R+1 (or +infinity if R=n).
    #
    # The number of operations for this segment will be (length of segment) - (length of such subsequence).
    #
    # To solve this efficiently:
    # For a fixed range [L, R] and bounds (low, high), we want the longest subsequence of a[L...R]
    # such that all elements are > low and < high, AND they are increasing.
    # Since the condition "all elements are > low and < high" is a global filter on the values,
    # we can first filter the array segment to only include values v where low < v < high.
    # Then find the LIS of the filtered array.
    #
    # However, n is up to 5*10^5. An O(N log N) solution is required.
    # The standard LIS algorithm is O(N log N).
    # We have multiple segments. Sum of lengths of segments is at most N.
    # So running LIS on each segment is efficient enough.
    
    # Step 0: Check fixed values consistency
    fixed_indices = sorted(list(b_set))
    if k > 0:
        for i in range(k - 1):
            if a[fixed_indices[i]] >= a[fixed_indices[i+1]]:
                print("-1")
                return
    # Also check if k=0, no fixed values, just need a[1] < ... < a[n] possible?
    # If k=0, we can change everything, so answer is 0? 
    # Wait, if k=0, we can change all elements to 1, 2, 3... So 0 operations.
    # But wait, the problem says "minimum number of operations". If we can make it increasing by changing 0 elements, then 0.
    # But if the original array is already increasing, 0.
    # If k=0, we can definitely make it increasing (change all to 1, 2, ...). But do we need to change any?
    # Only if it's not already increasing. But we can change ANY element.
    # Wait, if k=0, we can change ALL elements. So we can make it increasing with 0 operations IF it is already increasing.
    # If it is not, we might still need 0 operations? No, if it's not increasing, we must change at least one?
    # Actually, if k=0, we can change any element. Can we make it increasing by changing 0 elements? Only if it is already increasing.
    # If not, we need to change some. But we can change ALL to make it increasing. Is it possible to do it with fewer changes?
    # Yes, LIS.
    # So the logic holds: for k=0, the "fixed" boundaries are -inf and +inf. The whole array is one segment.
    # We find LIS of the whole array. Operations = n - LIS.
    
    # Let's formalize the segments.
    # Boundaries:
    # prev_val: -infinity (conceptually)
    # current fixed index: fixed_indices[0]
    # ...
    # After last fixed index: next_val = +infinity
    
    # Let's build a list of segments with their boundaries and the slice of the array.
    # Segment definition:
    # Start index L, End index R (inclusive)
    # Left bound: value at L-1 (if L>1 and L-1 in b, else -1e18)
    # Right bound: value at R+1 (if R<n and R+1 in b, else 1e18)
    
    segments = []
    
    if k == 0:
        # One segment [1, n]
        # Left bound: -inf, Right bound: +inf
        segments.append((1, n, -float('inf'), float('inf')))
    else:
        # Segment before first fixed
        first_fixed = fixed_indices[0]
        if first_fixed > 1:
            segments.append((1, first_fixed - 1, -float('inf'), a[first_fixed]))
        
        # Segments between fixed indices
        for i in range(k - 1):
            curr_fixed = fixed_indices[i]
            next_fixed = fixed_indices[i+1]
            start = curr_fixed + 1
            end = next_fixed - 1
            if start <= end:
                segments.append((start, end, a[curr_fixed], a[next_fixed]))
        
        # Segment after last fixed
        last_fixed = fixed_indices[-1]
        if last_fixed < n:
            segments.append((last_fixed + 1, n, a[last_fixed], float('inf')))
    
    total_ops = 0
    
    # Precompute a mapping from index to value for O(1) access? a is already 1-indexed list.
    # We need to be careful with the bounds.
    # For LIS, we filter values: low < val < high.
    # Then find LIS of the filtered sequence.
    
    for L, R, low, high in segments:
        # Extract values in this segment
        # We need indices L, L+1, ..., R
        # Filter: low < val < high
        # Then LIS
        
        # Optimization: if the segment is empty, continue
        if L > R:
            continue
            
        # Extract and filter
        # We can iterate directly
        # To implement LIS in O(M log M) where M is length of segment
        # We maintain a list 'tails' where tails[i] is the smallest tail of all increasing subsequences of length i+1.
        
        tails = []
        
        # Iterate through indices from L to R
        # We can access a[i] directly
        for idx in range(L, R + 1):
            val = a[idx]
            if val <= low or val >= high:
                continue
            
            # LIS step
            # Find the first element in tails >= val
            # Since tails is sorted, we can use bisect_left
            import bisect
            pos = bisect.bisect_left(tails, val)
            if pos == len(tails):
                tails.append(val)
            else:
                tails[pos] = val
        
        kept = len(tails)
        length_segment = R - L + 1
        ops = length_segment - kept
        total_ops += ops
        
    print(total_ops)

if __name__ == '__main__':
    solve()