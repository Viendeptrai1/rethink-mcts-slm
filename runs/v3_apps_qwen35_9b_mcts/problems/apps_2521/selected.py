import sys
import heapq

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    N = int(data[0])
    A = []
    for i in range(3 * N):
        A.append(int(data[1 + i]))
    
    # We need to choose 2N elements from 3N such that the first N form the first half
    # and the second N form the second half.
    # Let the split point in the original array be i (0-indexed).
    # This means we pick N elements from A[0...i] to be the first half,
    # and N elements from A[i+1...3N-1] to be the second half.
    # For the first half, we want to maximize the sum, so we pick the largest N elements.
    # For the second half, we want to minimize the sum, so we pick the smallest N elements.
    # The split point i must satisfy: i >= N-1 (to have at least N elements before or at i)
    # and i <= 2N-1 (to have at least N elements after i).
    
    # Precompute prefix max sums: max_sum_prefix[i] = max sum of N elements from A[0...i]
    # We can use a min-heap of size N to maintain the largest N elements seen so far.
    
    max_sum_prefix = [0] * (3 * N)
    min_heap = []
    
    # Fill for i from 0 to 2N-1 (since we need at least N elements to form the first half)
    # Actually, the split point i is the index of the last element included in the first part's source range.
    # Range for first part: 0 to i. We need i+1 >= N => i >= N-1.
    # Range for second part: i+1 to 3N-1. We need (3N-1) - (i+1) + 1 >= N => 3N - i - 1 >= N => 2N - 1 >= i => i <= 2N - 1.
    
    for i in range(3 * N):
        val = A[i]
        if len(min_heap) < N:
            heapq.heappush(min_heap, val)
        else:
            if val > min_heap[0]:
                heapq.heapreplace(min_heap, val)
        
        if i >= N - 1:
            max_sum_prefix[i] = sum(min_heap)
        else:
            max_sum_prefix[i] = -1  # Invalid state

    # Precompute suffix min sums: min_sum_suffix[i] = min sum of N elements from A[i...3N-1]
    # We can use a max-heap of size N to maintain the smallest N elements.
    # Python's heapq is a min-heap, so we store negative values.
    
    min_sum_suffix = [0] * (3 * N)
    max_heap = []  # Will store negative values
    
    # Fill for i from 2N to 3N-1 (since we need at least N elements starting from i)
    # Range for second part: i to 3N-1. We need 3N - i >= N => i <= 2N.
    # But the split point i is the end of the first part's source.
    # The second part source starts at i+1.
    # So we need min_sum_suffix[i+1].
    # Let's compute min_sum_suffix[j] for j from 2N down to 0.
    
    for j in range(3 * N - 1, -1, -1):
        val = A[j]
        if len(max_heap) < N:
            heapq.heappush(max_heap, -val)
        else:
            if -val > max_heap[0]:  # -val is the negative of current, max_heap stores negatives.
                # We want to keep the smallest N. If current val is smaller than the largest in our set (which is -max_heap[0]),
                # we replace.
                # max_heap[0] is the smallest negative, i.e., the largest positive value in our set of smallest N.
                if -val > max_heap[0]:
                    heapq.heapreplace(max_heap, -val)
        
        if len(max_heap) == N:
            min_sum_suffix[j] = -sum(max_heap)
        else:
            min_sum_suffix[j] = -1  # Invalid state

    ans = -float('inf')
    
    # Iterate over all valid split points i
    # First part source: 0 to i. Need i >= N-1.
    # Second part source: i+1 to 3N-1. Need 3N - (i+1) >= N => i <= 2N - 1.
    for i in range(N - 1, 2 * N):
        first_half_sum = max_sum_prefix[i]
        second_half_sum = min_sum_suffix[i + 1]
        
        if first_half_sum != -1 and second_half_sum != -1:
            score = first_half_sum - second_half_sum
            if score > ans:
                ans = score
    
    print(ans)

if __name__ == '__main__':
    solve()