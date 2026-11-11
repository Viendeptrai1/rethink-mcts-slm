import sys
import heapq

def largest_k_multiple_free_subset(n, k, a):
    # Sort the array to process elements in increasing order
    a.sort()
    
    # Initialize a max heap to keep track of the sizes of k-multiple free subsets
    max_heap = []
    
    for num in a:
        # Find the largest subset size that does not include a multiple of num/k
        while max_heap and max_heap[0][1] * k <= num:
            heapq.heappop(max_heap)
        
        # If the heap is empty, start a new subset with the current number
        if not max_heap:
            heapq.heappush(max_heap, (1, num))
        else:
            # Extend the largest valid subset by including the current number
            largest_size, _ = max_heap[0]
            heapq.heappush(max_heap, (largest_size + 1, num))
    
    # The size of the largest k-multiple free subset is the maximum value in the heap
    return max_heap[0][0]

# Read input from stdin
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:]))

# Print the result
print(largest_k_multiple_free_subset(n, k, a))