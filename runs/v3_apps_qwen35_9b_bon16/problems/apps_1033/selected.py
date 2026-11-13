import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    H = int(input_data[1])

    # Binary search for the minimum number of spots k
    # Range: [1, 2*n] because even with height 1 per spot, we need at most n spots.
    # Upper bound 2*n is safe because we can always construct a valid pyramid with height ~sqrt(2n) which takes ~2*sqrt(2n) spots, much less than 2n.
    
    def max_sand(k):
        # Calculate the maximum sand we can place in k spots satisfying:
        # h_1 <= H
        # |h_i - h_{i+1}| <= 1
        # h_i >= 0
        # To maximize sum, we want the sequence to be as large as possible.
        # The optimal shape for a fixed length k starting with h_1 <= H is:
        # Start at H (or less if H is too large relative to k, but we assume H is the cap)
        # Actually, the constraint is h_1 <= H. To maximize sum, we set h_1 = min(H, something).
        # But wait, the constraint is just h_1 <= H. The sequence can go up from there.
        # The "smoothest" way to maximize sum over k spots is to start as high as allowed and decrease by 1 each step?
        # No, we can also increase. But if we increase, we need more spots to sustain the height.
        # Actually, to maximize sum for a FIXED k, we should make the values as large as possible.
        # The constraints are local: |h_i - h_{i+1}| <= 1.
        # And h_1 <= H.
        # This implies h_i <= H + (i - 1).
        # Also, since h_i must be non-negative and we stop at k (implicitly h_{k+1}=0 is not required, 
        # but the problem says "minimum number of spots you can occupy". This implies h_k > 0 and h_{k+1} = 0.
        # So we must have h_{k+1} = 0.
        # Therefore, h_k <= 1, h_{k-1} <= 2, ..., h_1 <= k-1.
        # So h_i <= min(H + i - 1, k - i + 1) ??? No.
        
        # Let's re-evaluate the shape for max sand in k spots where h_{k+1}=0.
        # We need h_1 <= H.
        # We need |h_i - h_{i+1}| <= 1.
        # We need h_{k+1} = 0 (since only k spots are occupied, meaning h_k > 0 and h_{k+1} = 0).
        # To maximize sum, we want the sequence to be as high as possible.
        # Working backwards from h_{k+1}=0:
        # h_k <= 1
        # h_{k-1} <= 2
        # ...
        # h_i <= k - i + 1
        # Also working forwards from h_1:
        # h_1 <= H
        # h_2 <= H + 1
        # ...
        # h_i <= H + i - 1
        
        # So the upper bound for each h_i is min(H + i - 1, k - i + 1).
        # However, we must also ensure the sequence is valid (connected).
        # The sequence defined by b_i = min(H + i - 1, k - i + 1) is valid?
        # Let's check the difference:
        # Case 1: Both terms are increasing/decreasing in a way that maintains diff <= 1.
        # H+i-1 increases by 1.
        # k-i+1 decreases by 1.
        # The minimum of two lines with slopes +1 and -1 will have slope +1, then 0 (if they cross), then -1?
        # Actually, the min of two arithmetic progressions with step 1 and -1 will have a "mountain" shape.
        # The peak is where H+i-1 = k-i+1 => 2i = k - H + 2 => i = (k - H + 2)/2.
        # At the peak, the values are equal. Around the peak, the difference between consecutive terms is at most 1.
        # So the sequence b_i = min(H + i - 1, k - i + 1) is a valid sequence satisfying the slope constraint.
        # And it satisfies h_1 = min(H, k) <= H.
        # And h_{k+1} would be min(H+k, 0) = 0.
        # So this sequence is the maximal valid sequence for length k.
        
        # We need to calculate sum_{i=1 to k} min(H + i - 1, k - i + 1).
        
        # Let's find the intersection point.
        # H + i - 1 = k - i + 1
        # 2i = k - H + 2
        # i = (k - H + 2) / 2
        
        # Let peak_index be the integer i where the switch happens.
        # If k - H + 2 <= 0, then H >= k + something? 
        # If H is very large, then H + i - 1 is always >= k - i + 1 for i in [1, k]?
        # Check i=1: H >= k? If H >= k, then H+0 >= k. Yes.
        # So if H >= k, the min is always k - i + 1.
        # Sum = sum_{i=1 to k} (k - i + 1) = k + (k-1) + ... + 1 = k*(k+1)//2.
        
        # If H is small, there is a peak in the middle.
        # Let's define the two parts.
        # Part 1: i where H + i - 1 <= k - i + 1 => 2i <= k - H + 2 => i <= (k - H + 2) // 2.
        # Part 2: i where H + i - 1 > k - i + 1 => i > (k - H + 2) // 2.
        
        # Let limit = (k - H + 2) // 2.
        # If limit < 1, then for all i>=1, we are in Part 2.
        # If limit >= k, then for all i<=k, we are in Part 1. (This corresponds to H >= k roughly).
        
        limit = (k - H + 2) // 2
        
        if limit <= 0:
            # Entirely in the decreasing part (from the right perspective, or rather constrained by the right end 0)
            # h_i = k - i + 1
            # Sum = k*(k+1)//2
            return k * (k + 1) // 2
        
        if limit >= k:
            # Entirely in the increasing part (constrained by H)
            # h_i = H + i - 1
            # Sum = sum_{i=1}^k (H + i - 1) = k*H + (0 + 1 + ... + k-1) = k*H + k*(k-1)//2
            return k * H + k * (k - 1) // 2
        
        # Split at limit
        # For i from 1 to limit: h_i = H + i - 1
        # For i from limit+1 to k: h_i = k - i + 1
        
        # Sum1: sum_{i=1 to limit} (H + i - 1)
        # = limit*H + sum_{j=0}^{limit-1} j = limit*H + limit*(limit-1)//2
        
        sum1 = limit * H + limit * (limit - 1) // 2
        
        # Sum2: sum_{i=limit+1 to k} (k - i + 1)
        # Let j = k - i + 1.
        # When i = limit+1, j = k - (limit+1) + 1 = k - limit.
        # When i = k, j = 1.
        # So sum is sum_{j=1}^{k-limit} j = (k-limit)*(k-limit+1)//2
        
        sum2 = (k - limit) * (k - limit + 1) // 2
        
        return sum1 + sum2

    low = 1
    high = 2 * n  # Sufficiently large upper bound
    ans = high
    
    while low <= high:
        mid = (low + high) // 2
        if max_sand(mid) >= n:
            ans = mid
            high = mid - 1
        else:
            low = mid + 1
            
    print(ans)

if __name__ == '__main__':
    solve()