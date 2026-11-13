from typing import List

class Solution:
    def largestSumAfterKNegations(self, A: List[int], K: int) -> int:
        # Sort the array to bring the most negative numbers to the front
        A.sort()
        
        # Negate the smallest values K times
        for i in range(len(A)):
            if K > 0 and A[i] < 0:
                A[i] = -A[i]
                K -= 1
        
        # If K is still positive, we need to handle it
        # Sort the array again since we modified it
        A.sort()
        
        # If K is odd, flip the smallest element
        if K % 2 == 1:
            A[0] = -A[0]
        
        # Return the sum of the array
        return sum(A)