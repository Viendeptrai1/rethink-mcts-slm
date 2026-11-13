import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    b = []
    for i in range(n):
        b.append(int(data[1 + i]))
    
    if n == 2:
        # Deleting any single element from 2 elements leaves 1 element, which is always an AP
        print(1)
        return
    
    sorted_b = sorted(b)
    
    # Check if the sorted array is already an AP
    d = sorted_b[1] - sorted_b[0]
    valid = True
    for i in range(2, n):
        if sorted_b[i] - sorted_b[i-1] != d:
            valid = False
            break
    
    if valid:
        # It is an AP. We can remove either the first or the last element.
        # Removing the first element (index 1 in 1-based) works if n > 2 (which is true here)
        # Actually, if we remove the first element, the remaining is still an AP with same difference.
        # Same for the last.
        print(1)
        return
    
    # If not sorted AP, try to find which element to remove
    # The difference of the sorted array should be consistent except for one gap
    
    # Calculate the total range
    min_val = sorted_b[0]
    max_val = sorted_b[-1]
    
    # If there are only 2 distinct values, it might be that we have duplicates
    # But let's rely on the gap analysis
    
    # Check the number of unique elements
    unique_elements = sorted(list(set(b)))
    if len(unique_elements) == 1:
        # All elements are same. Removing any one leaves same elements -> AP with d=0
        print(1)
        return
    
    # We need to find the common difference d of the intended AP
    # d must be (max_val - min_val) / (n - 1 - (1 if we remove one end else 0))
    # Actually, simpler: if we remove one element, the remaining n-1 elements form an AP.
    # So (max_val - min_val) must be divisible by (n-1) if we remove an internal element?
    # Not necessarily. If we remove min_val or max_val, the range is smaller.
    
    # Let's try to determine the step d by looking at the sorted array gaps.
    # There should be at most one "large" gap or one element that doesn't fit.
    
    # Strategy:
    # 1. Check if removing sorted_b[0] makes the rest an AP.
    # 2. Check if removing sorted_b[-1] makes the rest an AP.
    # 3. Check if removing some internal element makes the rest an AP.
    
    # Function to check if a list is AP
    def is_ap(arr):
        k = len(arr)
        if k <= 2:
            return True
        d = arr[1] - arr[0]
        for i in range(2, k):
            if arr[i] - arr[i-1] != d:
                return False
        return True
    
    # Try removing first element of sorted array
    # But we need to return the original index.
    # We will map sorted_b back to original indices? No, we just need ANY index.
    # We can construct the candidate list from sorted_b, check, and if valid, find the original index.
    
    # However, finding the original index of a value in a list with duplicates is tricky.
    # But the problem asks for ANY index j.
    # If we decide to remove the element with value X, and there are multiple X's, removing any of them works.
    # So we just need to find one occurrence.
    
    # Let's try removing the smallest element (sorted_b[0])
    candidate = sorted_b[1:]
    if is_ap(candidate):
        # Find any index in original b that has value sorted_b[0]
        for idx, val in enumerate(b):
            if val == sorted_b[0]:
                print(idx + 1)
                return
    
    # Try removing the largest element (sorted_b[-1])
    candidate = sorted_b[:-1]
    if is_ap(candidate):
        for idx, val in enumerate(b):
            if val == sorted_b[-1]:
                print(idx + 1)
                return
    
    # Try removing an internal element.
    # The common difference d must be the GCD of adjacent differences? No.
    # If we remove one element, the remaining n-1 elements form an AP with some d.
    # This implies that (max_val - min_val) / (n - 2) might be d? 
    # Only if the removed element was not min or max.
    # But min and max are part of the AP unless the AP has length 1 (n=2, handled) or we remove min/max.
    # Wait, if we remove an internal element, the min and max remain.
    # So the remaining set is {min, ..., max} with one hole.
    # The number of elements is n-1. The number of steps from min to max is (n-1)-1 = n-2.
    # So d = (max_val - min_val) / (n - 2).
    # This d must be an integer.
    
    # Let's calculate potential d
    if (max_val - min_val) % (n - 2) != 0:
        # Cannot be an internal removal because min and max are preserved
        pass
    else:
        d = (max_val - min_val) // (n - 2)
        # Check if this d works
        # We need to check if sorted_b minus one element equals AP with d starting at min_val
        # Or simply, check if the sequence sorted_b can become AP by removing one element with step d.
        # We know min and max are kept.
        # So we expect the AP to be: min_val, min_val+d, ..., max_val
        # We iterate through the expected AP and match with sorted_b.
        # Count mismatches. If exactly one mismatch (meaning one element in sorted_b is extra), then that's our target.
        # But sorted_b has one extra element.
        # Let's reconstruct the expected AP of length n-1.
        # Expected elements: min_val + k*d for k in 0..n-2.
        # We can count how many elements in sorted_b match this pattern.
        # If count is n-1, then the one not matching is the one to remove.
        
        expected_set = set()
        for k in range(n - 1):
            expected_set.add(min_val + k * d)
        
        # Count matches
        matches = 0
        for x in sorted_b:
            if x in expected_set:
                matches += 1
        
        if matches == n - 1:
            # The missing one in expected_set (compared to sorted_b) is the one to remove.
            # Actually, sorted_b has n elements. expected_set has n-1 elements.
            # The element in sorted_b that is NOT in expected_set is the one to remove.
            for x in sorted_b:
                if x not in expected_set:
                    for idx, val in enumerate(b):
                        if val == x:
                            print(idx + 1)
                            return
    
    # If we haven't returned, then it's impossible
    print(-1)

if __name__ == "__main__":
    solve()