import sys
import heapq

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    N = int(next(iterator))
    
    # Read the 3N elements
    a = []
    for _ in range(3 * N):
        a.append(int(next(iterator)))
    
    # We need to choose 2N elements from 3N such that:
    # The first N chosen elements form the first half (maximize sum)
    # The last N chosen elements form the second half (minimize sum)
    # The relative order must be preserved.
    
    # Strategy:
    # Split the original array into two parts conceptually around a split point.
    # However, since we remove exactly N elements, the "split" between the first half and second half
    # of the new sequence a' can occur at any index i in the original array a, where i ranges from N to 2N.
    # Why?
    # - To have N elements in the first half of a', we must pick N elements from a[0...i-1].
    # - To have N elements in the second half of a', we must pick N elements from a[i...3N-1].
    # - The total elements picked is 2N. The total available is 3N. So we remove N.
    # - The split point i in the original array means:
    #   - We select N elements from the prefix a[0...i-1] (length i) to be the first half.
    #   - We select N elements from the suffix a[i...3N-1] (length 3N-i) to be the second half.
    # - For this to be possible, we need i >= N (to pick N from prefix) and 3N-i >= N => i <= 2N.
    
    # So we iterate i from N to 2N.
    # For a fixed i:
    #   Maximize sum of N elements from a[0...i-1] -> Take the N largest elements.
    #   Minimize sum of N elements from a[i...3N-1] -> Take the N smallest elements.
    #   Score = (Sum of N largest in prefix) - (Sum of N smallest in suffix).
    # We take the maximum score over all valid i.
    
    # To do this efficiently:
    # Precompute prefix max sums: For each length L from N to 2N, what is the max sum of N elements in a[0...L-1]?
    # Actually, we can compute an array `max_prefix_sum[k]` = max sum of N elements in a[0...k-1] for k in [N, 2N].
    # Similarly, `min_suffix_sum[k]` = min sum of N elements in a[k...3N-1] for k in [N, 2N].
    
    # Algorithm:
    # 1. Compute `max_prefix_sum` for split points i = N to 2N.
    #    We can maintain a min-heap of size N for the largest N elements seen so far.
    #    Iterate k from 0 to 2N-1.
    #    Add a[k] to heap. If heap size > N, pop the smallest (to keep largest N).
    #    When k reaches N-1, we have the first N elements. Record sum.
    #    Continue up to k = 2N-1. At each step k (where k+1 is the length of prefix), if k+1 >= N, we have a candidate.
    #    But we only care about split points i where we take N from prefix and N from suffix.
    #    Split point i means prefix is a[0...i-1] (length i). We need i >= N.
    #    So we compute max sum of N elements for prefixes of length N, N+1, ..., 2N.
    
    # 2. Compute `min_suffix_sum` for split points i = N to 2N.
    #    We need min sum of N elements from a[i...3N-1].
    #    Iterate backwards from 3N-1 down to N.
    #    Maintain a max-heap of size N for the smallest N elements.
    #    When we have processed enough elements to form a suffix of length >= N, we can record the min sum of N elements.
    #    Specifically, for a split point i, the suffix is a[i...3N-1]. Length = 3N - i.
    #    We need 3N - i >= N => i <= 2N.
    #    So we compute min sum of N elements for suffixes starting at i = 2N, 2N-1, ..., N.
    
    # Implementation details:
    # - Use a min-heap for the prefix part (to keep largest N, we pop smallest when size > N).
    # - Use a max-heap for the suffix part (to keep smallest N, we pop largest when size > N). In Python, use negative values.
    
    # Precompute prefix max sums
    # We need an array where index i corresponds to split point i (prefix length i).
    # Valid i: N, N+1, ..., 2N.
    # Let's create an array `pref` of size 3N+1, where pref[i] = max sum of N elements in a[0...i-1].
    # Initialize with -infinity or a flag for invalid.
    
    pref = [-float('inf')] * (3 * N + 1)
    
    # Min-heap to store the largest N elements seen so far
    # We store actual values. To get max sum of N, we keep the N largest.
    # When adding a new element, if we have < N, add it.
    # If we have N, compare new element with min of heap. If new > min, replace.
    heap = []
    current_sum = 0
    
    for i in range(3 * N):
        val = a[i]
        if len(heap) < N:
            heapq.heappush(heap, val)
            current_sum += val
        else:
            if val > heap[0]:
                removed = heapq.heappop(heap)
                current_sum -= removed
                heapq.heappush(heap, val)
                current_sum += val
        
        # If we have at least N elements, record the sum for split point i+1
        if len(heap) == N:
            pref[i + 1] = current_sum
            
    # Precompute suffix min sums
    # suf[i] = min sum of N elements in a[i...3N-1]
    # Valid i: N, N+1, ..., 2N.
    suf = [-float('inf')] * (3 * N + 1)
    
    # Max-heap to store the smallest N elements seen so far (from the right)
    # We store negative values to simulate max-heap with heapq (which is min-heap)
    heap = []
    current_sum = 0
    
    for i in range(3 * N - 1, -1, -1):
        val = a[i]
        # Push negative to simulate max-heap
        neg_val = -val
        if len(heap) < N:
            heapq.heappush(heap, neg_val)
            current_sum += val
        else:
            # heap[0] is the smallest negative, i.e., the largest actual value
            if neg_val < heap[0]:
                removed_neg = heapq.heappop(heap)
                current_sum -= (-removed_neg)
                heapq.heappush(heap, neg_val)
                current_sum += val
        
        if len(heap) == N:
            # The suffix starts at i, so split point is i.
            # We need suf[i]
            suf[i] = current_sum
            
    # Now iterate split point i from N to 2N
    max_score = -float('inf')
    
    for i in range(N, 2 * N + 1):
        # Check if both parts are valid
        if pref[i] != -float('inf') and suf[i] != -float('inf'):
            score = pref[i] - suf[i]
            if score > max_score:
                max_score = score
                
    print(max_score)

if __name__ == '__main__':
    solve()