from typing import List

class Solution:
    def largestSumAfterKNegations(self, A: List[int], K: int) -> int:
        for _ in range(K):
            A.sort()
            A[0] = -A[0]
        return sum(A)