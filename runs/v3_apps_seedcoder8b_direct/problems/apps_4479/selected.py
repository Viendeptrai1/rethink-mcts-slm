from typing import List

class Solution:
    def largestSumAfterKNegations(self, A: List[int], K: int) -> int:
        # Sort the array to bring negative numbers to the front
        A.sort()
        
        # Flip the negative numbers to positive, up to K times
        for i in range(len(A)):
            if K > 0 and A[i] < 0:
                A[i] = -A[i]
                K -= 1
        
        # If K is still odd, flip the smallest number
        if K % 2 == 1:
            A.sort()  # Sort again to find the smallest number
            A[0] = -A[0]
        
        # Return the sum of the modified array
        return sum(A)