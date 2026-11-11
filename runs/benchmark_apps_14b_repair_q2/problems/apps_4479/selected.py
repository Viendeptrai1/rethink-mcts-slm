class Solution:
    def largestSumAfterKNegations(self, A, K):
        for _ in range(K):
            min_index = A.index(min(A))
            A[min_index] = -A[min_index]
        return sum(A)