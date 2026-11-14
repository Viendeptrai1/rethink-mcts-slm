import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    idx = 0
    
    n = int(data[idx]); idx += 1
    k = int(data[idx]); idx += 1
    
    a = []
    for _ in range(n):
        a.append(int(data[idx])); idx += 1
    
    b_set = set()
    if k > 0:
        for _ in range(k):
            b_set.add(int(data[idx])); idx += 1
    
    # Identify fixed elements and their values
    # fixed_vals[i] will store the value of the i-th fixed element (0-indexed in the list of fixed elements)
    # fixed_indices[i] will store the original index (1-based) of the i-th fixed element
    fixed_indices = []
    fixed_vals = []
    
    for i in range(1, n + 1):
        if i in b_set:
            fixed_indices.append(i)
            fixed_vals.append(a[i-1])
    
    # Check if fixed elements themselves form a valid increasing sequence
    # Condition: fixed_vals[j] >= fixed_vals[j-1] + (fixed_indices[j] - fixed_indices[j-1])
    # Actually, since they must be strictly increasing and fit in the gaps, 
    # the minimum value at index i given previous value v at index p is v + (i - p).
    # So we need fixed_vals[j] >= fixed_vals[j-1] + (fixed_indices[j] - fixed_indices[j-1])
    
    for j in range(1, len(fixed_indices)):
        diff_idx = fixed_indices[j] - fixed_indices[j-1]
        diff_val = fixed_vals[j] - fixed_vals[j-1]
        if diff_val < diff_idx:
            print(-1)
            return
    
    # Now we need to select a subset of mutable elements (those not in b_set)
    # such that they can be part of a strictly increasing sequence along with fixed elements.
    # We want to maximize the number of kept mutable elements to minimize operations.
    
    # Let's define a DP or a greedy approach.
    # Since n is up to 5*10^5, O(n log n) is required.
    # This looks like a variation of LIS but with constraints on values relative to indices.
    
    # We can process the array in segments between fixed elements.
    # Segment 0: indices 1 to fixed_indices[0]-1
    # Segment j: indices fixed_indices[j-1]+1 to fixed_indices[j]-1
    # Segment last: indices fixed_indices[-1]+1 to n
    
    # For each segment, we have a range of indices [L, R] and a range of allowed values [min_val, max_val].
    # min_val is determined by the left anchor (or 1 if no left anchor).
    # max_val is determined by the right anchor (or infinity if no right anchor).
    # Specifically, if we keep an element at index i with value v, then:
    # v >= min_val + (i - L_start) where L_start is the index of the left anchor (or 1)
    # v <= max_val - (R_end - i) where R_end is the index of the right anchor (or n)
    # Also, the sequence of kept elements within the segment must be strictly increasing.
    # And the first kept element must satisfy the lower bound relative to left anchor,
    # and the last kept element must satisfy the upper bound relative to right anchor.
    # Moreover, any two kept elements at i and j (i < j) must satisfy v_j >= v_i + (j - i).
    
    # This condition v_j >= v_i + (j - i) is equivalent to (v_j - j) >= (v_i - i).
    # So if we transform the values: b_i = a_i - i, then the condition becomes b_j >= b_i.
    # So we are looking for a non-decreasing subsequence in terms of (a_i - i).
    # However, we also have absolute bounds on a_i.
    
    # Let's rephrase:
    # We want to find the longest subsequence of mutable elements such that:
    # 1. For any two selected elements at indices i < j with values v_i, v_j: v_j >= v_i + (j - i)
    # 2. If there is a left anchor at index L with value V_L, and the first selected element is at i:
    #    v_i >= V_L + (i - L)
    # 3. If there is a right anchor at index R with value V_R, and the last selected element is at j:
    #    v_j <= V_R - (R - j)
    # 4. The selected elements must be compatible with each other and the anchors.
    
    # Actually, the condition v_j >= v_i + (j - i) for ALL pairs in the subsequence (including anchors)
    # is equivalent to saying that the sequence of (value - index) is non-decreasing.
    # Let c_i = a_i - i. Then we need c_j >= c_i for i < j.
    # Also, the absolute value constraints translate to:
    # a_i >= V_L + (i - L)  =>  c_i + i >= V_L + i - L  =>  c_i >= V_L - L
    # a_i <= V_R - (R - i)  =>  c_i + i <= V_R - R + i  =>  c_i <= V_R - R
    
    # So for each segment between two anchors (or boundaries), we have:
    # Left bound for c_i: LB = (V_L - L) if left anchor exists, else -infinity
    # Right bound for c_i: RB = (V_R - R) if right anchor exists, else +infinity
    # We need to pick a subsequence of mutable elements in this segment such that:
    # 1. Their c_i values are non-decreasing.
    # 2. Each c_i is within [LB, RB].
    # 3. The first element picked has c_i >= LB.
    # 4. The last element picked has c_i <= RB.
    # 5. Additionally, the first element must be compatible with the left anchor (which is covered by LB)
    #    and the last with the right anchor (covered by RB).
    # But wait, if we pick multiple elements, say at i1, i2, ..., im, then:
    # c_i1 >= LB
    # c_im <= RB
    # c_i1 <= c_i2 <= ... <= c_im
    # This ensures compatibility with both anchors and internal consistency.
    
    # So the problem reduces to: for each segment, find the longest non-decreasing subsequence
    # of c_i values such that all values are in [LB, RB].
    # Since we want to maximize the total count, we can solve this for each segment independently
    # and sum the results.
    
    # Algorithm for a segment:
    # Given a list of (index, value) pairs for mutable elements in the segment.
    # Compute c = value - index.
    # Filter those with LB <= c <= RB.
    # Find the length of the longest non-decreasing subsequence of these c values.
    # Since we need non-decreasing, we can use the standard patience sorting / binary search approach for LIS.
    # For non-decreasing, when we encounter a value x, we find the first element in tails that is > x
    # and replace it with x. If no such element, append x.
    # Wait, standard LIS (strictly increasing) uses bisect_left.
    # For non-decreasing, we use bisect_right to find the first element > x, then replace.
    # Actually, let's verify:
    # Sequence: 1, 1, 2. Non-decreasing length 3.
    # tails: []
    # 1: bisect_right([], 1) -> 0. Append 1. tails=[1]
    # 1: bisect_right([1], 1) -> 1. Replace tails[1]? No, index 1 is out of bounds. Append 1. tails=[1, 1]
    # 2: bisect_right([1, 1], 2) -> 2. Append 2. tails=[1, 1, 2]. Length 3. Correct.
    # Sequence: 1, 2, 1.
    # 1: tails=[1]
    # 2: bisect_right([1], 2) -> 1. Append 2. tails=[1, 2]
    # 1: bisect_right([1, 2], 1) -> 1. Replace tails[1] with 1. tails=[1, 1]. Length 2. Correct (1,1 or 1,2).
    
    # So the algorithm for a segment is:
    # 1. Collect all mutable indices i in [L, R].
    # 2. Compute c_i = a[i] - i.
    # 3. Filter c_i such that LB <= c_i <= RB.
    # 4. Find LNDS length of the filtered c_i list.
    
    # However, there is a catch: the "first" element of the subsequence must be >= LB,
    # and the "last" must be <= RB. Our filtering does exactly that.
    # But what if the segment has no mutable elements? Then length is 0.
    # What if the segment has mutable elements but none satisfy [LB, RB]? Length 0.
    
    # One more thing: The problem asks for minimum operations.
    # Total operations = (Total mutable elements) - (Max kept mutable elements).
    # Total mutable elements = n - k.
    # Max kept = sum of LNDS lengths for each segment.
    
    # Let's implement this.
    
    total_mutable = n - k
    kept_count = 0
    
    # Helper for LNDS length
    def get_lnds_length(values):
        if not values:
            return 0
        tails = []
        for x in values:
            # Find first element in tails that is > x
            # bisect_right returns insertion point after all elements <= x
            # So tails[idx] will be the first element > x
            import bisect
            idx = bisect.bisect_right(tails, x)
            if idx < len(tails):
                tails[idx] = x
            else:
                tails.append(x)
        return len(tails)
    
    # Process segments
    # Segment 0: before first fixed element
    if k > 0:
        L = 1
        R = fixed_indices[0] - 1
        if L <= R:
            LB = -float('inf')
            RB = fixed_vals[0] - fixed_indices[0]
            # Collect mutable elements
            c_list = []
            for i in range(L, R + 1):
                if i not in b_set:
                    c_val = a[i-1] - i
                    if LB <= c_val <= RB:
                        c_list.append(c_val)
            kept_count += get_lnds_length(c_list)
        
        # Segments between fixed elements
        for j in range(1, k):
            L = fixed_indices[j-1] + 1
            R = fixed_indices[j] - 1
            if L <= R:
                LB = fixed_vals[j-1] - fixed_indices[j-1]
                RB = fixed_vals[j] - fixed_indices[j]
                c_list = []
                for i in range(L, R + 1):
                    if i not in b_set:
                        c_val = a[i-1] - i
                        if LB <= c_val <= RB:
                            c_list.append(c_val)
                kept_count += get_lnds_length(c_list)
        
        # Segment after last fixed element
        L = fixed_indices[-1] + 1
        R = n
        if L <= R:
            LB = fixed_vals[-1] - fixed_indices[-1]
            RB = float('inf')
            c_list = []
            for i in range(L, R + 1):
                if i not in b_set:
                    c_val = a[i-1] - i
                    if LB <= c_val <= RB:
                        c_list.append(c_val)
            kept_count += get_lnds_length(c_list)
    else:
        # No fixed elements
        # The entire array is one segment with no bounds on c_i?
        # Actually, if no fixed elements, we just need a strictly increasing sequence.
        # Condition: a_j >= a_i + (j - i) for all i < j in subsequence.
        # Equivalent to c_j >= c_i where c_i = a_i - i.
        # So we just need LNDS of c_i for all mutable elements.
        # No LB or RB constraints.
        c_list = []
        for i in range(1, n + 1):
            if i not in b_set:
                c_val = a[i-1] - i
                c_list.append(c_val)
        kept_count += get_lnds_length(c_list)
    
    print(total_mutable - kept_count)

if __name__ == '__main__':
    solve()