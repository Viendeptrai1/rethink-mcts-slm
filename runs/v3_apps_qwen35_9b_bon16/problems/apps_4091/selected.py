import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    a = []
    for i in range(n):
        a.append(int(data[2 + i]))
    
    # Find the k largest elements in the array
    # We need to identify the indices of the k largest values
    # Since we can only take contiguous segments, the optimal strategy is:
    # 1. Find the k-th largest value in the array. Let this be threshold.
    # 2. All elements strictly greater than threshold will definitely be included in separate segments (or contribute their value).
    # 3. Elements equal to the threshold will fill the remaining gaps to ensure we have exactly k segments.
    # Actually, a simpler greedy approach:
    # We want to maximize sum of max of each segment.
    # The maximum possible profit is the sum of the k largest values in the array.
    # Why? Because each segment contributes exactly one value (its max), and we have k segments.
    # To maximize the sum, we should try to make each segment's max one of the largest available numbers.
    # Since the array is fixed and we partition it contiguously, we can always achieve the sum of the k largest values.
    # Strategy:
    # 1. Find the k largest values. Sort them in descending order.
    # 2. The answer is the sum of these k values.
    # 3. To construct the partition:
    #    - We need to form k groups.
    #    - We will include the k largest elements as the "representative" (maximum) of each group.
    #    - We traverse the array and start a new group whenever we encounter one of the top k elements that hasn't been used as a group starter yet.
    #    - However, multiple occurrences of the same value might exist. We need to be careful.
    
    # Refined Strategy:
    # 1. Identify the k largest values. Let's call the sorted unique values or just the k largest items with their original indices.
    # 2. Actually, we don't need indices for the calculation, just the values.
    # 3. Calculation: Sort `a` in descending order. The max profit is sum(a[:k]).
    # 4. Construction:
    #    We need to output k lengths.
    #    We will select k indices in the original array `a` that correspond to the k largest values.
    #    If there are ties, any set of k indices corresponding to the k largest values works.
    #    Let's pick the indices of the k largest values. If there are ties, we can pick the first k occurrences of the values needed.
    #    Wait, simply picking any k indices for the top k values might not form contiguous groups if we just pick them.
    #    But the rule is: we cut the array into k contiguous pieces. The max of each piece is one of the numbers in the array.
    #    The set of maxima of the k pieces must be a subset of the array.
    #    To maximize the sum, we want the set of maxima to be exactly the k largest values of the array.
    #    Can we always achieve this? Yes.
    #    Algorithm for construction:
    #    1. Sort the array `a` descending to find the k-th largest value, say `limit`.
    #    2. Collect all indices where `a[i] > limit`. These MUST be the maxima of their respective groups.
    #    3. We need `k` groups. Suppose there are `m` elements strictly greater than `limit`. We need `k - m` more groups.
    #    4. We can take any `k - m` elements equal to `limit` to serve as the maxima for the remaining groups.
    #    5. So, identify the set of indices that will be the "peaks". These are all indices with value > limit, plus (k - count_of_greater) indices with value == limit.
    #    6. Sort these peak indices.
    #    7. The first group ends at the first peak index. The second group starts after the first peak index and ends at the second peak index, etc.
    #    8. The last group goes from the last peak index to the end of the array.
    #    9. Verify: The max of the segment [start, peak_i] is >= a[peak_i]. Since a[peak_i] is one of the largest, and any element before it in the current segment is either a previous peak (handled) or smaller, the max will be a[peak_i] (assuming we don't include a larger element from a future peak, which we don't because peaks are sorted).
    #       Wait, if there is an element larger than `limit` BEFORE the current peak but we didn't pick it as a peak? 
    #       No, we picked ALL elements > limit as peaks. So any element before a peak in the current segment must be <= limit (or a previous peak which is part of the previous segment).
    #       Actually, if we have indices p1, p2, ..., pk (sorted).
    #       Segment 1: 0 to p1. Max is max(a[0...p1]). Since p1 is a peak, a[p1] is one of the top k. Any element before p1 is either a previous peak (none for first) or <= limit. And since p1 is the first peak, no element > limit exists before p1. So max is a[p1].
    #       Segment i: p_{i-1} + 1 to p_i. Max is max(a[p_{i-1}+1 ... p_i]). Any element here is <= limit? 
    #       If there was an element > limit in between, it would have been in our list of peaks, so it would be p_i itself (since we sorted peaks).
    #       So yes, the max of segment i is a[p_i].
    #       Segment k: p_{k-1} + 1 to n-1. Max is max(a[p_{k-1}+1 ... n-1]). Similar logic, no element > limit exists after p_{k-1} because we included all of them in peaks.
    
    # Implementation steps:
    # 1. Create a list of (value, index) pairs.
    # 2. Sort this list descending by value.
    # 3. Take the first k elements. These are our chosen peaks.
    # 4. Extract the indices and sort them.
    # 5. Generate the lengths of the segments.
    
    # Edge case: k=1. We take the max element. One segment 0 to n-1.
    
    # Let's refine the selection of k peaks when there are ties.
    # If we have values [10, 10, 10] and k=2. Sorted: (10,0), (10,1), (10,2).
    # We pick first 2: indices 0 and 1.
    # Peaks: [0, 1].
    # Segments: [0..0] (len 1), [1..n-1] (len n-1).
    # Max of [0..0] is 10. Max of [1..n-1] is 10. Sum = 20. Correct.
    
    # What if we picked indices 0 and 2?
    # Peaks: [0, 2].
    # Segments: [0..0], [1..2].
    # Max of [0..0] is 10. Max of [1..2] is 10 (since a[2]=10, a[1]=10). Sum = 20. Correct.
    # So picking the first k in sorted order (stable or not) works.
    
    # Data preparation
    indexed_a = [(a[i], i) for i in range(n)]
    # Sort descending by value
    indexed_a.sort(key=lambda x: x[0], reverse=True)
    
    # Select top k
    top_k = indexed_a[:k]
    
    # Sort by index to determine boundaries
    peak_indices = sorted([idx for val, idx in top_k])
    
    # Calculate total profit
    total_profit = sum(val for val, idx in top_k)
    
    # Calculate segment lengths
    lengths = []
    current_start = 0
    for idx in peak_indices:
        length = idx - current_start + 1
        lengths.append(length)
        current_start = idx + 1
    
    # The last segment goes to the end
    # Wait, the loop above handles the segments ending at each peak.
    # We have k peaks, so we generate k lengths?
    # Let's trace:
    # peaks = [p1, p2, ..., pk]
    # i=0: end at p1, len = p1 - 0 + 1. start becomes p1+1.
    # i=1: end at p2, len = p2 - (p1+1) + 1 = p2 - p1. start becomes p2+1.
    # ...
    # i=k-1: end at pk, len = pk - (p_{k-1}+1) + 1. start becomes pk+1.
    # This generates k segments. The last one ends at pk.
    # But we need to cover the rest of the array up to n-1.
    # The problem says we solve ALL n problems.
    # The peaks are just the points where the max is achieved.
    # The segment containing the last peak must extend to the end of the array.
    # My logic above: "Segment k: p_{k-1} + 1 to n-1".
    # But in the loop I stopped at pk.
    # So the last segment should be from (prev_peak + 1) to n-1.
    # Let's re-verify the loop logic.
    # If peaks = [p1, p2]. k=2.
    # Loop 1: idx=p1. len = p1+1. start = p1+1.
    # Loop 2: idx=p2. len = p2 - (p1+1) + 1 = p2 - p1. start = p2+1.
    # This leaves the part from p2+1 to n-1 unsolved?
    # Ah, the max of the segment ending at p2 is a[p2]. If we extend the segment to n-1, the max is still a[p2] (since no larger values exist after p2).
    # So the last segment must go to n-1.
    # Correct logic:
    # The segments are defined by the peaks.
    # Segment 1: 0 to p1
    # Segment 2: p1+1 to p2
    # ...
    # Segment k: p_{k-1}+1 to n-1
    # So the last length is (n-1) - (p_{k-1}+1) + 1 = n - 1 - p_{k-1}.
    # In my loop, the last iteration calculates length ending at pk.
    # So I need to adjust the last length.
    
    lengths = []
    current_start = 0
    # Iterate through first k-1 peaks to set boundaries
    for i in range(k - 1):
        idx = peak_indices[i]
        length = idx - current_start + 1
        lengths.append(length)
        current_start = idx + 1
    
    # Last segment
    last_idx = peak_indices[-1]
    last_length = n - current_start
    lengths.append(last_length)
    
    print(total_profit)
    print(*(lengths))

if __name__ == '__main__':
    solve()