import sys
import heapq

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    N = int(next(iterator))
    
    a = []
    for _ in range(3 * N):
        a.append(int(next(iterator)))
    
    # We need to choose 2N elements: N for the first half (maximize sum) and N for the second half (minimize sum).
    # The split point between the first N chosen and the next N chosen can be anywhere from index N to 2N (0-indexed) in the original array.
    # Specifically, if we split the original array at index i (meaning we take i elements from the start for the first half candidates,
    # and the rest from i onwards for the second half candidates), we need to ensure:
    # - We pick exactly N elements from a[0...i-1] for the first half.
    # - We pick exactly N elements from a[i...3N-1] for the second half.
    # To maximize the score: Sum(first half) - Sum(second half), we want to maximize the sum of the first half
    # and minimize the sum of the second half.
    #
    # For a fixed split index i:
    # - The best N elements from a[0...i-1] are the largest N. We can get their sum by taking the sum of the largest N in the prefix.
    #   Actually, to compute this efficiently for all i, we can maintain the sum of the largest N elements seen so far.
    #   Since we need the largest N, we can use a min-heap of size N to keep track of the largest N elements.
    # - The best N elements from a[i...3N-1] for the second half (which we want to minimize) are the smallest N.
    #   We can precompute the sum of the smallest N elements in each suffix starting from i. We can use a max-heap for this.
    
    # Let's define:
    # prefix_max_sum[i]: maximum sum of N elements chosen from a[0...i-1] (i must be >= N)
    # suffix_min_sum[i]: minimum sum of N elements chosen from a[i...3N-1] (i must be <= 2N)
    #
    # The answer is max over i from N to 2N of: prefix_max_sum[i] - suffix_min_sum[i]
    
    # Compute prefix_max_sum
    # We iterate i from 0 to 3N.
    # We need prefix_max_sum[i] for i >= N.
    # We maintain a min-heap of the largest N elements seen so far.
    
    min_heap = []  # stores the largest N elements seen so far (as a min-heap)
    current_sum = 0
    prefix_max_sum = [0] * (3 * N + 1)
    
    for i in range(3 * N):
        val = a[i]
        if len(min_heap) < N:
            heapq.heappush(min_heap, val)
            current_sum += val
        else:
            if val > min_heap[0]:
                removed = heapq.heappop(min_heap)
                current_sum -= removed
                heapq.heappush(min_heap, val)
                current_sum += val
            # else: val is smaller than or equal to the smallest of the top N, so we ignore it for the "largest N" set.
        
        # prefix_max_sum[i+1] corresponds to having processed i+1 elements (indices 0 to i)
        # If we have processed at least N elements, we have a valid set of N largest.
        if len(min_heap) == N:
            prefix_max_sum[i + 1] = current_sum
        else:
            prefix_max_sum[i + 1] = -1  # Invalid state, should not happen for i >= N-1
    
    # Compute suffix_min_sum
    # We iterate from the end.
    # We need suffix_min_sum[i] for i from 0 to 2N (specifically we will use i from N to 2N).
    # We maintain a max-heap of the smallest N elements in the current suffix.
    # In Python, heapq is a min-heap, so we store negative values to simulate a max-heap.
    
    max_heap = []  # stores negative of the smallest N elements (simulating max-heap)
    current_sum_neg = 0
    suffix_min_sum = [0] * (3 * N + 1)
    
    for i in range(3 * N - 1, -1, -1):
        val = a[i]
        if len(max_heap) < N:
            heapq.heappush(max_heap, -val)
            current_sum_neg += val
        else:
            # We want to keep the smallest N. If current val is smaller than the largest of the current smallest N (which is -max_heap[0]),
            # we replace the largest.
            if -max_heap[0] > val:
                removed_neg = heapq.heappop(max_heap)
                current_sum_neg -= (-removed_neg)
                heapq.heappush(max_heap, -val)
                current_sum_neg += val
            # else: val is larger, so we don't include it in the smallest N set.
        
        # suffix_min_sum[i] corresponds to suffix starting at i.
        if len(max_heap) == N:
            suffix_min_sum[i] = current_sum_neg
        else:
            suffix_min_sum[i] = -1  # Invalid
    
    # Calculate maximum score
    # We can split at index i, meaning we take N from a[0...i-1] and N from a[i...3N-1].
    # Valid split indices i are from N to 2N (inclusive).
    # Because:
    # - To pick N from left, we need at least N elements: i >= N.
    # - To pick N from right, we need at least N elements from i to end: (3N - i) >= N => i <= 2N.
    
    max_score = -float('inf')
    
    for i in range(N, 2 * N + 1):
        left_sum = prefix_max_sum[i]
        right_sum = suffix_min_sum[i]
        score = left_sum - right_sum
        if score > max_score:
            max_score = score
            
    print(max_score)

if __name__ == '__main__':
    solve()