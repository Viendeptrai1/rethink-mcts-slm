import sys
import heapq

def max_items_without_horn(n, X, prices):
    # Sort the prices in ascending order
    prices.sort()
    
    # Use a min-heap to keep track of the smallest sums of pairs
    min_heap = []
    
    # Iterate through the prices and try to form pairs
    for i in range(n):
        for j in range(i + 1, n):
            pair_sum = prices[i] + prices[j]
            # If the pair sum is greater than X, we cannot include both items
            if pair_sum > X:
                # Push the pair sum into the heap
                heapq.heappush(min_heap, pair_sum)
                # If the heap size exceeds n, pop the largest element
                if len(min_heap) > n:
                    heapq.heappop(min_heap)
    
    # The size of the heap is the maximum number of items we can mark
    return len(min_heap)

# Read input from stdin
input = sys.stdin.read
data = input().split()

n = int(data[0])
X = int(data[1])
prices = list(map(int, data[2:]))

# Print the result
print(max_items_without_horn(n, X, prices))