from typing import List
import heapq

class Solution:
    def largestSumAfterKNegations(self, A: List[int], K: int) -> int:
        # Use a min-heap to always access the smallest element
        heapq.heapify(A)
        
        # Flip the sign of the smallest element K times
        # But we need to be careful: if we flip a negative number, it becomes positive
        # and might become the new smallest (or largest positive)
        # Strategy:
        # 1. Always flip the current minimum element.
        # 2. If the minimum is negative, flipping it increases the sum.
        # 3. If the minimum is positive, flipping it decreases the sum.
        #    However, since we want to maximize the sum, we should only flip positive numbers
        #    if we have no choice (i.e., we still have K operations left and all numbers are positive).
        #    In that case, flipping the smallest positive number is the best we can do to minimize the loss.
        
        for _ in range(K):
            if A[0] < 0:
                heapq.heappop(A)
                val = -heapq.heappop(A) # This is wrong logic above, let's fix
                # Actually, let's pop, negate, and push back
                val = heapq.heappop(A)
                if val < 0:
                    heapq.heappush(A, -val)
                else:
                    heapq.heappush(A, val)
            else:
                # If the smallest is non-negative, we must flip the smallest one to minimize the reduction
                val = heapq.heappop(A)
                heapq.heappush(A, -val)
        
        return sum(A)

# Wait, the logic inside the loop has a bug. Let me rewrite it cleanly.
# Correct approach:
# 1. Sort the array or use a heap to find the smallest element.
# 2. If the smallest element is negative, flip it and decrement K.
# 3. If the smallest element is positive (or zero), flip it and decrement K.
#    But note: flipping a negative number makes it positive, which might be larger than other numbers.
#    So after flipping a negative number, we should re-evaluate the smallest element.
#    Using a heap automatically handles this because after pushing back the negated value,
#    the heap property is maintained (min-heap will bring the next smallest to the top).

class Solution:
    def largestSumAfterKNegations(self, A: List[int], K: int) -> int:
        heapq.heapify(A)
        
        for _ in range(K):
            val = heapq.heappop(A)
            if val < 0:
                heapq.heappush(A, -val)
            else:
                # If the smallest is non-negative, flipping it reduces the sum.
                # But we have to do it if K > 0. We flip the smallest positive to minimize the loss.
                heapq.heappush(A, -val)
        
        return sum(A)