import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = []
    for i in range(n):
        a.append(int(input_data[1 + i]))

    # We need to find the number of subarrays [l, r] with length >= 2 such that:
    # sum(a[l..r]) == product(a[l..r])
    #
    # Key observations:
    # 1. If a subarray contains any number >= 2, the product grows very fast.
    #    Specifically, if there are k numbers >= 2, the product is at least 2^k.
    #    The sum is at most (max_val) * k.
    #    For the product to equal the sum, the subarray cannot be too long if it contains large numbers.
    # 2. If a subarray contains only 1s, then sum = length, product = 1.
    #    So sum == product implies length == 1. But we need length >= 2.
    #    Therefore, a valid subarray cannot consist entirely of 1s.
    # 3. If a subarray contains at least one number >= 2, let's analyze the constraints.
    #    Let the subarray be S. Let P = product(S), Q = sum(S).
    #    If S contains a number x >= 2, then P >= x.
    #    Also, if S has length L and contains m numbers >= 2 (m >= 1), then P >= 2^m.
    #    Q <= L * max(S).
    #    Since max(S) <= 10^9, L can be up to 2*10^5.
    #    However, if there are two or more numbers >= 2, say x and y (both >= 2),
    #    then P >= x*y >= 4.
    #    Consider the case where we have a block of 1s and a few numbers >= 2.
    #    Let the non-1 numbers be b_1, b_2, ..., b_m.
    #    The sum is (count_of_1s) + sum(b_i).
    #    The product is product(b_i).
    #    So: count_of_1s + sum(b_i) = product(b_i)
    #    => count_of_1s = product(b_i) - sum(b_i)
    #    Since count_of_1s >= 0, we must have product(b_i) >= sum(b_i).
    #    This is generally true for integers >= 2, except for small cases like [2] (2=2), [2,2] (4>4? no 4>4 is false, 4=4? no 4>4), wait.
    #    [2]: prod=2, sum=2. count_1s = 0. Valid if length>=2? No, length is 1.
    #    [2, 2]: prod=4, sum=4. count_1s = 0. Length = 2. Valid!
    #    [2, 1]: prod=2, sum=3. count_1s = -1. Impossible.
    #    [1, 2]: prod=2, sum=3. Impossible.
    #    [2, 2, 1]: prod=4, sum=5. Impossible.
    #    [2, 2, 2]: prod=8, sum=6. count_1s = 2. So [1, 1, 2, 2, 2] -> sum=7, prod=8. No.
    #    Wait, the equation is: count_1s = prod - sum.
    #    For [2, 2]: prod=4, sum=4, count_1s=0. Subarray [2, 2]. Sum=4, Prod=4. Match.
    #    For [2, 2, 1]: prod=4, sum=5. count_1s = -1. Impossible.
    #    For [1, 2, 2]: prod=4, sum=5. Impossible.
    #    For [1, 1, 2, 2]: prod=4, sum=6. Impossible.
    #    For [2, 2, 1, 1]: prod=4, sum=6. Impossible.
    #    For [2, 2, 2]: prod=8, sum=6. count_1s = 2.
    #       So if we have two 1s and three 2s: [1, 1, 2, 2, 2]. Sum = 2+6=8. Prod=8. Match.
    #    For [2, 2, 2, 2]: prod=16, sum=8. count_1s = 8.
    #       So [1]*8 + [2,2,2,2]. Sum = 8+8=16. Prod=16. Match.
    #
    #    General strategy:
    #    Iterate over all possible contiguous subarrays of non-1 numbers.
    #    Let this subarray be B. Calculate P = product(B), S = sum(B).
    #    We need to find how many 1s can be attached to B (on left or right) such that:
    #    (number of 1s) + S = P  => number of 1s = P - S.
    #    Let K = P - S.
    #    If K < 0, then no solution for this B.
    #    If K >= 0, we need to check if there are at least K ones available adjacent to B.
    #    Specifically, if B starts at index i and ends at index j (0-based) in the original array a,
    #    then the ones must be in the range [i-K1, i-1] and [j+1, j+K2] such that K1+K2 = K.
    #    The number of available ones to the left is L_ones = i (if a[0..i-1] are all 1s? No, just consecutive ones ending at i-1).
    #    Actually, we can precompute the length of consecutive 1s ending at each position and starting at each position.
    #    Let left_ones[i] = number of consecutive 1s ending at i-1.
    #    Let right_ones[i] = number of consecutive 1s starting at i+1.
    #    Actually, simpler:
    #    Precompute an array `consecutive_ones` where `consecutive_ones[i]` is the length of the run of 1s ending at i.
    #    And another array `next_non_one[i]` which is the index of the next non-1 number after i.
    #    Or even simpler:
    #    Identify all maximal contiguous segments of non-1 numbers.
    #    For each such segment B (from index L to R), calculate P and S.
    #    If P == S, then we need 0 ones. The number of ways is (number of ways to choose 0 ones from left) * (number of ways to choose 0 ones from right)?
    #    No, the problem asks for the number of subarrays.
    #    A subarray is defined by its start and end.
    #    If we fix the core non-1 part from L to R, and we need K = P - S ones.
    #    We can take x ones from the left (where 0 <= x <= available_left) and y ones from the right (where 0 <= y <= available_right) such that x + y = K.
    #    The number of ways for this specific core is the number of pairs (x, y) satisfying the conditions.
    #    This is max(0, min(available_left, K) - max(0, K - available_right) + 1).
    #    Wait, let's re-verify.
    #    We need x + y = K.
    #    Constraints: 0 <= x <= L_avail, 0 <= y <= R_avail.
    #    Substitute y = K - x.
    #    0 <= K - x <= R_avail  =>  K - R_avail <= x <= K.
    #    Also 0 <= x <= L_avail.
    #    So max(0, K - R_avail) <= x <= min(K, L_avail).
    #    Number of solutions = max(0, min(K, L_avail) - max(0, K - R_avail) + 1).
    #
    #    What if P == S? Then K=0.
    #    x+y=0 => x=0, y=0. One way (the core itself).
    #    Formula: min(0, L) - max(0, -R) + 1 = 0 - 0 + 1 = 1. Correct.
    #
    #    What if the entire array is 1s?
    #    Then there are no non-1 segments. The loop over non-1 segments won't run.
    #    But we need to check if there are any valid subarrays of all 1s.
    #    For all 1s, sum = length, prod = 1.
    #    sum == prod => length == 1.
    #    But we need length >= 2. So no solutions for all-1s arrays.
    #    So if the array has no non-1 numbers, answer is 0.
    #
    #    Algorithm:
    #    1. Identify segments of consecutive non-1 numbers.
    #    2. For each segment, compute product and sum.
    #       Since numbers can be up to 10^9 and segment length can be large, product can exceed 64-bit integer.
    #       However, note that if product exceeds sum + max_possible_ones, we can stop.
    #       Max possible ones is n (2*10^5).
    #       Max sum is roughly n * 10^9 = 2*10^14.
    #       So if product > 2*10^14 + 2*10^5, we can cap it or break.
    #       Actually, if product > sum + n, then K = P - S > n, which is impossible since max ones is n.
    #       So we can cap the product at sum + n + 1.
    #    3. Calculate K = P - S.
    #    4. If K < 0, ignore.
    #    5. Count available ones on left and right of the segment.
    #    6. Add the number of valid (x, y) pairs to the total.
    #
    #    Complexity:
    #    We iterate through the array once to find segments.
    #    For each segment, we compute product and sum.
    #    The product can grow exponentially. We break early if it gets too large.
    #    Since we break early, the inner loop runs very few times for large numbers.
    #    For small numbers (like 1s, but we skip 1s in segments), the only small non-1 is 2.
    #    If we have many 2s, say k 2s, product = 2^k.
    #    We stop when 2^k > sum + n.
    #    sum <= 2*k. So 2^k > 2k + n.
    #    For n=2*10^5, 2^k > 4*10^5 => k approx 19.
    #    So the length of any segment we fully process is very small (<= ~20-30).
    #    Thus, the total complexity is O(n).

    # Precompute consecutive ones to the left and right?
    # Actually, we can just scan.
    # Let's create a list of segments of non-1s.
    # Each segment is (start_index, end_index).
    # We also need to know the number of consecutive 1s immediately to the left of start_index
    # and immediately to the right of end_index.
    
    # Let's build an array `is_one` or just process directly.
    # We can iterate i from 0 to n-1.
    # If a[i] == 1, continue.
    # If a[i] != 1, start a new segment.
    # Find the end of the segment.
    # Process the segment.
    # Then continue.

    total_ways = 0
    i = 0
    n_val = n
    a_list = a

    while i < n_val:
        if a_list[i] == 1:
            i += 1
            continue
        
        # Start of a non-1 segment
        start = i
        prod = 1
        s_sum = 0
        
        # We will extend as long as we have non-1s
        # But we must be careful about overflow and early termination
        # Also, we need to know the exact end of the contiguous non-1 block to count surrounding 1s correctly.
        # So first, find the end of the block.
        j = i
        while j < n_val and a_list[j] != 1:
            j += 1
        end = j - 1
        
        # Now process the segment from i to end
        # Calculate product and sum, with early break if product gets too large
        current_prod = 1
        current_sum = 0
        possible = True
        
        for k in range(i, end + 1):
            val = a_list[k]
            current_sum += val
            # Check for overflow relative to max possible needed
            # Max needed product is current_sum + n_val (approx)
            # If current_prod > current_sum + n_val, then K = prod - sum > n_val, impossible.
            # But we need to be careful: current_sum increases.
            # Let's use a safe upper bound. Max sum is 2e5 * 1e9 = 2e14.
            # Max ones is 2e5.
            # So if current_prod > 2e14 + 2e5, we can stop.
            # Let's use a slightly larger bound to be safe, e.g., 4e14.
            if current_prod > 400000000000000: # 4e14
                possible = False
                break
            current_prod *= val
        
        if not possible:
            # Product was too huge, no solution for this segment or any extension
            i = end + 1
            continue
        
        K = current_prod - current_sum
        
        if K < 0:
            i = end + 1
            continue
        
        # Count ones to the left
        left_ones = 0
        if i > 0:
            # Check how many consecutive 1s end at i-1
            temp = i - 1
            while temp >= 0 and a_list[temp] == 1:
                left_ones += 1
                temp -= 1
        
        # Count ones to the right
        right_ones = 0
        if end < n_val - 1:
            temp = end + 1
            while temp < n_val and a_list[temp] == 1:
                right_ones += 1
                temp += 1
        
        # Calculate number of ways
        # We need x + y = K, 0 <= x <= left_ones, 0 <= y <= right_ones
        # x in [max(0, K - right_ones), min(K, left_ones)]
        lower = max(0, K - right_ones)
        upper = min(K, left_ones)
        
        if upper >= lower:
            total_ways += (upper - lower + 1)
        
        i = end + 1

    print(total_ways)

if __name__ == '__main__':
    solve()