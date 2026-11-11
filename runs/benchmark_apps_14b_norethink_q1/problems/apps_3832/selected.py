import sys
import heapq

def min_hours_to_build_houses(n, heights):
    # Calculate the ceiling of n/2
    max_k = (n + 1) // 2
    
    # Initialize the result list with infinity
    result = [float('inf')] * max_k
    
    # Create a max-heap to store the differences between consecutive hills
    heap = []
    
    # Calculate the differences between consecutive hills
    for i in range(1, n):
        diff = heights[i] - heights[i - 1]
        if diff > 0:
            heapq.heappush(heap, -diff)
    
    # Calculate the minimum hours required for each k
    total_hours = 0
    for k in range(max_k):
        if heap:
            # Get the largest difference (smallest negative value in the heap)
            largest_diff = -heapq.heappop(heap)
            total_hours += largest_diff
        result[k] = total_hours
    
    return result

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
heights = list(map(int, data[1:]))

# Calculate and print the result
result = min_hours_to_build_houses(n, heights)
print(" ".join(map(str, result)))