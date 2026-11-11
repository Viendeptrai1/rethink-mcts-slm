import sys
import heapq

def min_instability(n, a):
    # Find the minimum and maximum values in the array
    min_val = min(a)
    max_val = max(a)
    
    # If all elements are the same, the instability is already 0
    if min_val == max_val:
        return 0
    
    # Create a min-heap and a max-heap
    min_heap = []
    max_heap = []
    
    for num in a:
        heapq.heappush(min_heap, num)
        heapq.heappush(max_heap, -num)
    
    # Remove the smallest element
    smallest = heapq.heappop(min_heap)
    # Remove the largest element
    largest = -heapq.heappop(max_heap)
    
    # Calculate the instability after removing the smallest element
    instability1 = max_val - heapq.heappop(min_heap)
    # Calculate the instability after removing the largest element
    instability2 = -heapq.heappop(max_heap) - min_val
    
    # Return the minimum of the two calculated instabilities
    return min(instability1, instability2)

# Read input
n = int(sys.stdin.readline())
a = list(map(int, sys.stdin.readline().split()))

# Print the result
print(min_instability(n, a))