from heapq import heappush, heappop

class Solution:
    def largestSumAfterKNegations(self, A: List[int], K: int) -> int:
        # Use a min-heap to efficiently access the smallest element
        heap = []
        for num in A:
            heappush(heap, num)
        
        # Perform K negations
        for _ in range(K):
            # Get the smallest element
            smallest = heappop(heap)
            # Negate it and push back
            heappush(heap, -smallest)
        
        # Calculate the sum of the modified array
        return sum(heap)