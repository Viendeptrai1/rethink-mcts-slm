from typing import List

class Solution:
    def largestSumAfterKNegations(self, A: List[int], K: int) -> int:
        # Sort the array to bring negative numbers to the front
        A.sort()
        
        # Negate the smallest negative numbers first
        for i in range(len(A)):
            if K > 0 and A[i] < 0:
                A[i] = -A[i]
                K -= 1
        
        # If there are remaining negations, apply them to the smallest element
        if K > 0:
            A.sort()  # Sort again to find the smallest element
            A[0] = -A[0] if K % 2 == 1 else A[0]
        
        # Return the sum of the modified array
        return sum(A)