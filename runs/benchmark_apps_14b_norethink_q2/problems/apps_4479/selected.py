class Solution:
    def largestSumAfterKNegations(self, A, K):
        # Sort the array to handle negative numbers first
        A.sort()
        
        # Flip the negative numbers until we run out of flips or there are no more negatives
        for i in range(len(A)):
            if A[i] < 0 and K > 0:
                A[i] = -A[i]
                K -= 1
        
        # If K is still greater than 0 and is odd, flip the smallest number
        if K % 2 == 1:
            A.sort()
            A[0] = -A[0]
        
        # Return the sum of the array
        return sum(A)