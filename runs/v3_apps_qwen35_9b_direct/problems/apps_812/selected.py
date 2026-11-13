import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    b = list(map(int, input_data[1:]))
    
    if n == 2:
        print(1)
        return
    
    # Sort the array to easily check for arithmetic progression
    sorted_b = sorted(b)
    
    # Calculate differences between adjacent elements
    diffs = [sorted_b[i+1] - sorted_b[i] for i in range(n-1)]
    
    # Count occurrences of each difference
    from collections import Counter
    diff_counts = Counter(diffs)
    
    # Case 1: All differences are the same (already an AP)
    # We can remove any element. The problem asks for any index.
    # Removing the first element (index 1) is always valid if it's already an AP.
    if len(diff_counts) == 1:
        print(1)
        return
    
    # Case 2: Two types of differences
    # The AP might have a common difference 'd', and we removed one element causing a gap of 2d.
    # Or we removed an element from the end/start causing a different issue.
    
    # Get the two unique differences
    unique_diffs = list(diff_counts.keys())
    
    # If there are more than 2 unique differences, it's impossible to fix by removing one element
    if len(unique_diffs) > 2:
        print(-1)
        return
    
    d1, d2 = unique_diffs[0], unique_diffs[1]
    
    # Check if one difference is exactly twice the other (indicating a missing element in the middle)
    # Or if the counts suggest removing an element from the start/end
    
    # Strategy: Try removing elements that correspond to the "outlier" differences
    # The candidate indices to try are those where the difference is d2 (the less frequent one usually)
    # or at the boundaries.
    
    # Let's identify potential candidates based on the differences
    # If we remove an element, the new common difference should be consistent.
    
    # Possible scenarios:
    # 1. The common difference is d1, and we have one occurrence of d2 = 2*d1 (missing middle element)
    # 2. The common difference is d2, and we have one occurrence of d1 = 2*d2 (missing middle element)
    # 3. The common difference is d1, and we removed an element from the start or end (only 1 outlier diff)
    # 4. The common difference is d2, and we removed an element from the start or end
    
    # Let's try to verify if removing a specific element works.
    # Candidates:
    # - Indices where the difference is d2 (if d2 is the "bad" one)
    # - First element (index 0)
    # - Last element (index n-1)
    
    candidates = set()
    
    # If d2 is much larger than d1, maybe d1 is the true step and d2 is 2*d1
    if d2 == 2 * d1:
        # Try removing the element that causes the jump d2
        # Find index i such that sorted_b[i+1] - sorted_b[i] == d2
        for i in range(n-1):
            if diffs[i] == d2:
                candidates.add(i + 1) # 1-based index
                break
        # Also try removing first or last if needed, but usually the gap indicates the middle
        # However, if the gap is at the very beginning or end, it might be different.
        # But if d2 = 2*d1, the gap is internal.
    
    elif d1 == 2 * d2:
        for i in range(n-1):
            if diffs[i] == d1:
                candidates.add(i + 1)
                break
    
    # If the counts are 1 and n-2, it could be removing first or last element
    # Example: [1, 3, 5, 7, 10] -> diffs [2, 2, 2, 3]. d1=2, d2=3. Not 2x.
    # Example: [1, 2, 4, 5] -> diffs [1, 2, 1]. d1=1, d2=2. d2=2*d1. Remove 4 (index 3).
    # Example: [1, 3, 5, 7] -> AP. Handled above.
    # Example: [1, 2, 3, 5] -> diffs [1, 1, 2]. d1=1, d2=2. Remove 5 (index 4).
    # Example: [1, 5, 9] -> diffs [4, 4]. AP.
    # Example: [1, 2, 4, 8] -> diffs [1, 2, 4]. 3 unique diffs -> -1.
    
    # Special case: Only one difference type but counts are not uniform? No, if len==1, handled.
    
    # Another case: The common difference is d, and we removed an element from the start.
    # Then we have one diff of 2d at the beginning.
    # e.g., [2, 4, 6, 8] remove 2 -> [4, 6, 8] (AP). Original diffs: [2, 2, 2]. Wait, if original is AP, handled.
    # e.g., [1, 3, 5, 7] remove 1 -> [3, 5, 7] (AP). Original diffs: [2, 2, 2]. Handled.
    # e.g., [1, 2, 4, 5] -> diffs [1, 2, 1]. d1=1, d2=2. d2=2*d1. Candidate index 3 (value 4).
    # e.g., [1, 3, 5, 7, 9] remove 9 -> [1, 3, 5, 7] (AP). Original diffs [2,2,2,2]. Handled.
    # e.g., [1, 2, 3, 5] -> diffs [1, 1, 2]. d1=1, d2=2. d2=2*d1. Candidate index 4 (value 5).
    
    # What if the outlier is at the start?
    # [1, 3, 5, 7] -> AP.
    # [1, 2, 4, 5] -> diffs [1, 2, 1]. Gap in middle.
    # [1, 5, 9] -> diffs [4, 4]. AP.
    # [1, 2, 3, 4, 6] -> diffs [1, 1, 1, 2]. d1=1, d2=2. Gap at end. Remove 6.
    
    # What if the outlier is at the start?
    # [1, 3, 5, 7] -> AP.
    # [1, 2, 4, 5] -> diffs [1, 2, 1].
    # [1, 3, 5, 7] remove 1 -> [3, 5, 7]. Original was AP.
    # Consider [1, 2, 4, 5, 6] -> diffs [1, 2, 1, 1]. d1=1, d2=2. Remove 4.
    # Consider [1, 3, 5, 7, 9] -> AP.
    # Consider [1, 2, 3, 5, 7] -> diffs [1, 1, 2, 2]. Two 2s. len(diff_counts)=2, counts {1:2, 2:2}.
    # This implies two gaps of 2d? Or d=1 and we have two missing? Impossible with 1 removal.
    # So if counts are not 1 and n-2, and not 2 and 1 (for the larger diff), it might fail.
    
    # Let's refine candidates:
    # 1. If d2 == 2 * d1: candidate is the index where diff is d2.
    # 2. If d1 == 2 * d2: candidate is the index where diff is d1.
    # 3. If the larger difference appears only once, it could be at the start or end.
    #    But if it's at the start, the first diff is 2d, then d, d...
    #    If it's at the end, ..., d, d, 2d.
    #    In these cases, the "bad" diff is the only one of its kind.
    #    So if count of max(d1, d2) is 1, we try removing the element before or after that diff.
    
    # Let's collect all potential indices to try
    potential_indices = []
    
    # If there is a difference that is exactly twice the other
    if d2 == 2 * d1:
        # Try removing the element that creates the gap d2
        for i in range(n-1):
            if diffs[i] == d2:
                potential_indices.append(i + 1)
                break
    elif d1 == 2 * d2:
        for i in range(n-1):
            if diffs[i] == d1:
                potential_indices.append(i + 1)
                break
    
    # If the counts are such that one difference appears once, it might be at the boundary
    # e.g., [1, 2, 4, 5] -> diffs [1, 2, 1]. d1=1, d2=2. count(2)=1. Index of 2 is 2 (0-based) -> element 3 (1-based).
    # e.g., [1, 3, 5, 7, 9] -> AP.
    # e.g., [1, 2, 3, 5] -> diffs [1, 1, 2]. d1=1, d2=2. count(2)=1. Index of 2 is 2 -> element 4.
    # e.g., [1, 3, 5, 7] remove 1 -> [3, 5, 7]. Original diffs [2, 2, 2].
    # e.g., [1, 2, 4, 5, 6] -> diffs [1, 2, 1, 1]. d1=1, d2=2. count(2)=1. Index of 2 is 1 -> element 2.
    # Wait, [1, 2, 4, 5, 6] sorted is same. Remove 4 (index 3). Diffs: 1, 2, 1, 1. Gap is 2.
    # What if the gap is at the start? [1, 3, 5, 7] -> AP.
    # What if [1, 2, 3, 4, 6]? Diffs [1, 1, 1, 2]. Gap at end. Remove 6.
    # What if [1, 3, 5, 7, 9] remove 1? Original is AP.
    # What if [1, 2, 4, 5]? Diffs [1, 2, 1]. Gap in middle.
    
    # Is it possible the gap is at the start?
    # Sequence: [1, 3, 5, 7]. Remove 1 -> [3, 5, 7]. Original diffs [2, 2, 2].
    # Sequence: [1, 2, 4, 5]. Remove 1 -> [2, 4, 5] -> diffs [2, 1]. Not AP.
    # Sequence: [1, 2, 3, 5]. Remove 1 -> [2, 3, 5] -> diffs [1, 2]. Not AP.
    # Sequence: [1, 2, 3, 4, 6]. Remove 6 -> [1, 2, 3, 4] -> AP.
    # Sequence: [1, 2, 3, 5, 7]. Remove 5 -> [1, 2, 3, 7] -> diffs [1, 1, 4]. No.
    # Sequence: [1, 2, 3, 5, 7]. Remove 3? [1, 2, 5, 7] -> [1, 3, 2]. No.
    
    # It seems the gap (2d) is always internal if d is the true step.
    # Unless the true step is d/2?
    # e.g., [1, 2, 4, 5]. True step 1. Gap 2.
    # e.g., [1, 3, 5, 7]. True step 2.
    # e.g., [1, 2, 3, 4, 6]. True step 1. Gap 2 at end.
    
    # What if the true step is d2 and d1 is the gap?
    # e.g., [1, 3, 5, 7, 9] remove 9 -> [1, 3, 5, 7]. Diffs [2, 2, 2].
    # e.g., [1, 2, 4, 5]. Diffs [1, 2, 1]. d1=1, d2=2. True step 1.
    # e.g., [1, 3, 5, 7]. Diffs [2, 2, 2].
    # e.g., [1, 2, 3, 5]. Diffs [1, 1, 2]. True step 1.
    
    # What if the sequence is [1, 2, 4, 8]? Diffs [1, 2, 4]. 3 unique. -1.
    
    # Let's just try the candidates we found and also the first and last elements if the counts suggest boundary removal.
    # If count of the larger difference is 1, it could be at the start or end.
    # If count of the larger difference is 1, and it's at the start, removing the first element might work.
    # If it's at the end, removing the last element might work.
    
    # Let's add first and last indices to candidates if the larger diff count is 1.
    if len(diff_counts) == 2:
        max_diff = max(d1, d2)
        min_diff = min(d1, d2)
        if diff_counts[max_diff] == 1:
            potential_indices.append(1) # Try removing first
            potential_indices.append(n) # Try removing last
    
    # Also, if the smaller diff count is 1, it might be a boundary issue too?
    # e.g., [1, 2, 4, 5]. Diffs [1, 2, 1]. max=2, count=1. min=1, count=2.
    # e.g., [1, 3, 5, 7, 9] -> AP.
    # e.g., [1, 2, 3, 5]. Diffs [1, 1, 2]. max=2, count=1.
    
    # What if the sequence is [1, 2, 3, 4, 6]? Diffs [1, 1, 1, 2]. max=2, count=1.
    # Candidates: index of 2 (4), first (1), last (5).
    # Removing 4 (value 6) works.
    
    # What if [1, 3, 5, 7, 9] remove 1? Original is AP.
    # What if [1, 2, 4, 5] remove 1? [2, 4, 5] -> [2, 2, 1]. No.
    # What if [1, 2, 4, 5] remove 5? [1, 2, 4] -> [1, 2, 2]. No.
    # So only removing 4 works.
    
    # What if [1, 2, 3, 5, 7]? Diffs [1, 1, 2, 2]. Two 2s. Fails.
    
    # Let's implement a helper to check if a list is AP
    def is_ap(arr):
        if len(arr) <= 2:
            return True
        d = arr[1] - arr[0]
        for i in range(2, len(arr)):
            if arr[i] - arr[i-1] != d:
                return False
        return True
    
    # Try each candidate
    for idx in potential_indices:
        # Create new list without element at idx-1 (0-based)
        new_b = b[:idx-1] + b[idx:]
        # Sort to check AP property (since we can reorder)
        new_b_sorted = sorted(new_b)
        if is_ap(new_b_sorted):
            print(idx)
            return
    
    print(-1)

if __name__ == '__main__':
    solve()