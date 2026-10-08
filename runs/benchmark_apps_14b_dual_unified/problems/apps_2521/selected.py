import sys
import heapq

def max_score(N, a):
    # Calculate prefix sums
    prefix_sum = [0] * (3 * N + 1)
    for i in range(1, 3 * N + 1):
        prefix_sum[i] = prefix_sum[i - 1] + a[i - 1]
    
    # Max-heap to store the negative values for the first half
    max_heap = []
    # Min-heap to store the values for the second half
    min_heap = []
    
    # Initialize the heaps with the first N elements
    for i in range(N):
        heapq.heappush(max_heap, -a[i])
        heapq.heappush(min_heap, a[N + i])
    
    # Calculate the initial score
    current_score = (-sum(max_heap)) - sum(min_heap)
    max_score = current_score
    
    # Slide the window across the array
    for i in range(N, 2 * N):
        # Remove the element that is sliding out of the first half
        remove_element = -heapq.heappop(max_heap)
        prefix_sum[i] -= remove_element
        
        # Add the new element to the first half
        heapq.heappush(max_heap, -a[i])
        
        # Remove the element that is sliding out of the second half
        remove_element = heapq.heappop(min_heap)
        prefix_sum[2 * N + i - N] -= remove_element
        
        # Add the new element to the second half
        heapq.heappush(min_heap, a[2 * N + i - N])
        
        # Update the current score
        current_score = prefix_sum[2 * N] - prefix_sum[N] - prefix_sum[3 * N] + prefix_sum[2 * N]
        
        # Update the maximum score
        max_score = max(max_score, current_score)
    
    return max_score

# Read input
input = sys.stdin.read
data = input().split()
N = int(data[0])
a = list(map(int, data[1:]))

# Print the result
print(max_score(N, a))