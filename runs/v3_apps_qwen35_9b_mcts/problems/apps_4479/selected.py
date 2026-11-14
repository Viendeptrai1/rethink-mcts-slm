from typing import List
import heapq

class Solution:
    def largestSumAfterKNegations(self, A: List[int], K: int) -> int:
        # Sort the array to easily access negative numbers and smallest absolute values
        A.sort()
        
        # Flip negative numbers to positive as long as we have K moves
        for i in range(len(A)):
            if K > 0 and A[i] < 0:
                A[i] = -A[i]
                K -= 1
            else:
                break
        
        # If we still have moves left (K > 0), it means all numbers are non-negative.
        # We must flip the smallest number K times.
        # Flipping a positive number twice returns to original, so only parity of K matters.
        if K > 0:
            if K % 2 == 1:
                # Find the minimum element and flip it once
                min_val = min(A)
                # Since we need to reduce the sum by 2 * min_val, we can just subtract 2*min_val from the total sum
                # But easier: flip the actual element in the list
                # However, we need to be careful: the minimum might not be at index 0 if we flipped some negatives.
                # Actually, after flipping negatives, the array is sorted in non-decreasing order of absolute values?
                # Not necessarily. Example: [-5, -2, 3] -> [5, 2, 3]. Sorted: [2, 3, 5].
                # We need the minimum absolute value in the current array.
                # Since we sorted initially, and flipped negatives, the smallest absolute value is either:
                # 1. The first element if it was originally negative and flipped (now positive)
                # 2. The first element if it was originally non-negative
                # Actually, after flipping all negatives, the array is not necessarily sorted.
                # Better approach: find the minimum element in the current array.
                A[0] = -A[0]  # Flip the smallest element (since array might not be sorted after flips, we find min)
                # Wait, the above logic is flawed. Let's restart the logic for the remaining K.
        
        # Correct approach for remaining K:
        # After flipping all negatives, the array contains only non-negative numbers.
        # We need to flip the smallest number if K is odd.
        # But wait, the array might not be sorted after flipping.
        # Let's re-calculate:
        
        # Re-sort or find min
        # Actually, we can just find the minimum element in the current array A
        if K > 0:
            if K % 2 == 1:
                min_val = min(A)
                # We need to flip the element with value min_val
                # But which index? Any index with that value.
                # To minimize the sum reduction, we flip the smallest value.
                # The sum will be reduced by 2 * min_val.
                # So we can just calculate the sum and subtract 2 * min_val.
                # But we need to modify the array? The problem says "modify the array", but we just need the sum.
                # However, to be safe, let's find the index of the minimum and flip it.
                idx = A.index(min_val)
                A[idx] = -A[idx]
        
        return sum(A)

# Wait, the above logic has a flaw in the initial flipping part.
# Let's rewrite the solution more carefully.

class Solution:
    def largestSumAfterKNegations(self, A: List[int], K: int) -> int:
        # Sort the array
        A.sort()
        
        # Flip negative numbers to positive
        for i in range(len(A)):
            if K > 0 and A[i] < 0:
                A[i] = -A[i]
                K -= 1
            else:
                break
        
        # If K is still > 0, it means all numbers are non-negative.
        # We need to flip the smallest number if K is odd.
        if K > 0:
            if K % 2 == 1:
                # Find the minimum element in the current array
                min_val = min(A)
                # Flip the minimum element
                # We need to find an index with this value and flip it
                # Since the array might not be sorted after flipping, we search
                for i in range(len(A)):
                    if A[i] == min_val:
                        A[i] = -A[i]
                        break
        
        return sum(A)

# Wait, there's still an issue. After flipping negatives, the array is not necessarily sorted.
# Example: A = [-5, -2, 3], K = 2
# After sorting: [-5, -2, 3]
# Flip -5 -> [5, -2, 3], K=1
# Flip -2 -> [5, 2, 3], K=0
# Sum = 10. Correct.

# Example: A = [-5, -2, 3], K = 1
# After sorting: [-5, -2, 3]
# Flip -5 -> [5, -2, 3], K=0
# Sum = 6. Correct.

# Example: A = [3, -1, 0, 2], K = 3
# Sorted: [-1, 0, 2, 3]
# Flip -1 -> [1, 0, 2, 3], K=2
# Now all non-negative. K=2 (even), so no more flips needed.
# Sum = 6. Correct.

# Example: A = [2, -3, -1, 5, -4], K = 2
# Sorted: [-4, -3, -1, 2, 5]
# Flip -4 -> [4, -3, -1, 2, 5], K=1
# Flip -3 -> [4, 3, -1, 2, 5], K=0
# Sum = 13. Correct.

# But what if we have remaining K and the array is not sorted?
# Example: A = [-5, 1, 2], K = 2
# Sorted: [-5, 1, 2]
# Flip -5 -> [5, 1, 2], K=1
# Now all non-negative. K=1 (odd), so flip the smallest.
# Smallest is 1. Flip -> [5, -1, 2]. Sum = 6.
# Is this optimal? 
# Original: [-5, 1, 2]
# Option 1: Flip -5 -> [5, 1, 2], then flip 1 -> [5, -1, 2]. Sum = 6.
# Option 2: Flip -5 -> [5, 1, 2], then flip 2 -> [5, 1, -2]. Sum = 4.
# Option 3: Flip 1 -> [-5, -1, 2], then flip -5 -> [5, -1, 2]. Sum = 6.
# So yes, flipping the smallest absolute value is correct.

# But in my code, after flipping negatives, the array is not sorted.
# So I need to find the minimum element correctly.
# The min() function will work correctly.

# However, there's a better approach:
# Instead of modifying the array in place and then searching for min,
# we can track the minimum absolute value during the process.

# Let's rewrite with a cleaner approach:

class Solution:
    def largestSumAfterKNegations(self, A: List[int], K: int) -> int:
        # Sort the array
        A.sort()
        
        # Flip negative numbers to positive
        for i in range(len(A)):
            if K > 0 and A[i] < 0:
                A[i] = -A[i]
                K -= 1
            else:
                break
        
        # If K is still > 0, it means all numbers are non-negative.
        # We need to flip the smallest number if K is odd.
        if K > 0:
            if K % 2 == 1:
                # Find the minimum element in the current array
                min_val = min(A)
                # Flip the minimum element
                for i in range(len(A)):
                    if A[i] == min_val:
                        A[i] = -A[i]
                        break
        
        return sum(A)

# This should work. Let's test with the examples.

# Example 1: A = [4,2,3], K = 1
# Sorted: [2, 3, 4]
# No negatives. K=1 (odd). Flip min (2) -> [-2, 3, 4]. Sum = 5. Correct.

# Example 2: A = [3,-1,0,2], K = 3
# Sorted: [-1, 0, 2, 3]
# Flip -1 -> [1, 0, 2, 3], K=2
# All non-negative. K=2 (even). No flip. Sum = 6. Correct.

# Example 3: A = [2,-3,-1,5,-4], K = 2
# Sorted: [-4, -3, -1, 2, 5]
# Flip -4 -> [4, -3, -1, 2, 5], K=1
# Flip -3 -> [4, 3, -1, 2, 5], K=0
# Sum = 13. Correct.

# One more test: A = [-5, 1, 2], K = 2
# Sorted: [-5, 1, 2]
# Flip -5 -> [5, 1, 2], K=1
# All non-negative. K=1 (odd). Flip min (1) -> [5, -1, 2]. Sum = 6. Correct.

# Another test: A = [-5, 1, 2], K = 3
# Sorted: [-5, 1, 2]
# Flip -5 -> [5, 1, 2], K=2
# All non-negative. K=2 (even). No flip. Sum = 8. Correct.

# The solution looks correct.

class Solution:
    def largestSumAfterKNegations(self, A: List[int], K: int) -> int:
        A.sort()
        
        for i in range(len(A)):
            if K > 0 and A[i] < 0:
                A[i] = -A[i]
                K -= 1
            else:
                break
        
        if K > 0 and K % 2 == 1:
            min_val = min(A)
            for i in range(len(A)):
                if A[i] == min_val:
                    A[i] = -A[i]
                    break
        
        return sum(A)