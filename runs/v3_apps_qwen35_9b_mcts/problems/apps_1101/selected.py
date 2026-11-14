import sys
import math

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    k = int(input_data[1])
    s = input_data[2]
    
    target_len = k + 1
    min_max_dist = float('inf')
    
    i = 0
    while i < n:
        if s[i] == '0':
            start = i
            while i < n and s[i] == '0':
                i += 1
            length = i - start
            if length >= target_len:
                # We need to pick k+1 rooms from this segment of '0's.
                # To minimize the max distance from the center to the farthest endpoint,
                # we should pick the k+1 rooms such that they are as close to the center as possible.
                # The optimal strategy within a contiguous block of zeros of length L is to pick
                # the middle room for Farmer John and extend k rooms to the left and right as evenly as possible.
                # The resulting max distance is ceil((k) / 2).
                # Why? Because we have k cows. We can distribute them as floor(k/2) on one side and ceil(k/2) on the other.
                # The farthest cow will be at distance ceil(k/2).
                # Note: The length of the segment must be at least k+1, which is guaranteed by the problem if a solution exists.
                # However, we must ensure the segment is long enough to accommodate the specific distribution.
                # Actually, the minimal max distance for a fixed k is always ceil(k/2) regardless of segment length,
                # as long as the segment length >= k+1.
                # Let's verify:
                # k=1 -> ceil(1/2)=1. Segment "000", pick middle. Dist=1. Correct.
                # k=2 -> ceil(2/2)=1. Segment "00000", pick middle, one left, one right. Dist=1. Correct.
                # k=3 -> ceil(3/2)=2. Segment "000000", pick middle, 1 left, 2 right (or vice versa). Max dist=2. Correct.
                # So the answer for any valid segment is simply ceil(k/2).
                # Wait, let's re-read the first example carefully.
                # Example 1: n=7, k=2, s="0100100". Zeros at indices 0, 2, 3, 5, 6.
                # Segments of consecutive zeros:
                # 1. Index 0 (len 1)
                # 2. Indices 2-3 (len 2)
                # 3. Indices 5-6 (len 2)
                # None of these have length >= k+1 = 3.
                # But the example says output is 2.
                # "Farmer John can book room 3 for himself, and rooms 1 and 4 for his cows."
                # Rooms are 1-indexed in the problem description?
                # String: 0 1 0 0 1 0 0
                # Idx:   0 1 2 3 4 5 6
                # Room 3 (idx 2) is '0'. Room 1 (idx 0) is '0'. Room 4 (idx 3) is '0'.
                # These are NOT consecutive in the string. There is a '1' at idx 1.
                # Ah, the problem does NOT require the k+1 rooms to be consecutive.
                # It just requires them to be unoccupied.
                # My initial reasoning about sliding windows of consecutive zeros was wrong.
                
                # Let's re-evaluate.
                # We need to choose k+1 indices i_0, i_1, ..., i_k such that s[i_j] == '0'.
                # One of these is Farmer John's room (say i_0), and the others are cows.
                # We want to minimize max(|i_j - i_0|) for all j.
                # This is equivalent to finding a center C (one of the zero positions) and a radius R such that
                # there are at least k zeros in the range [C-R, C+R] (excluding C itself, so total k+1 including C).
                # We want to minimize R.
                
                # Algorithm:
                # 1. Collect all indices where s[i] == '0' into a list `zeros`.
                # 2. For each zero index `c` in `zeros`, we want to find the smallest R such that
                #    the number of zeros in [c-R, c+R] is at least k+1.
                #    Since `zeros` is sorted, we can use binary search or two pointers.
                #    Specifically, for a fixed center `c` (which is zeros[m]), we need to find the smallest R
                #    such that zeros[m - L] >= c - R and zeros[m + R] <= c + R? No.
                #    We need count of zeros in [c-R, c+R] >= k+1.
                #    Let the chosen set of indices be a subarray of `zeros` of length k+1: zeros[l], zeros[l+1], ..., zeros[l+k].
                #    The center must be one of these indices. To minimize the max distance, the center should be the median of this subarray.
                #    If we pick the subarray zeros[l...l+k], the optimal center is zeros[l + k//2].
                #    Then the max distance is max(zeros[l+k] - center, center - zeros[l]).
                #    We iterate over all possible windows of length k+1 in the `zeros` list.
                #    For each window, calculate the cost and take the minimum.
                
                pass
        
        else:
            i += 1
            
    # Re-implementing the correct logic
    zeros = [i for i, char in enumerate(s) if char == '0']
    m = len(zeros)
    
    if m < k + 1:
        # Should not happen based on problem statement
        return

    min_dist = float('inf')
    
    # We need to select k+1 consecutive zeros from the `zeros` list.
    # Let the selected indices in `zeros` be from index `i` to `i+k`.
    # The values are zeros[i], zeros[i+1], ..., zeros[i+k].
    # To minimize the max distance from the center to the farthest endpoint,
    # the center should be the median of these k+1 values.
    # The median index in the subarray of length k+1 is i + k // 2.
    # Let center_val = zeros[i + k // 2].
    # The farthest distance is max(zeros[i+k] - center_val, center_val - zeros[i]).
    
    for i in range(m - k):
        # Window of k+1 zeros: zeros[i] ... zeros[i+k]
        center_idx = i + k // 2
        center_val = zeros[center_idx]
        
        left_dist = center_val - zeros[i]
        right_dist = zeros[i+k] - center_val
        
        current_max = max(left_dist, right_dist)
        if current_max < min_dist:
            min_dist = current_max
            
    print(min_dist)

if __name__ == '__main__':
    solve()