import sys
import heapq

def max_score(N, a):
    # Calculate prefix sums
    prefix_sum = [0] * (3 * N + 1)
    for i in range(1, 3 * N + 1):
        prefix_sum[i] = prefix_sum[i - 1] + a[i - 1]
    
    # Min-heap to keep track of the smallest elements in the first half
    min_heap_first_half = []
    # Max-heap to keep track of the largest elements in the second half (using negative values)
    max_heap_second_half = []
    
    # Initialize the heaps with the first N elements
    for i in range(N):
        heapq.heappush(min_heap_first_half, a[i])
        heapq.heappush(max_heap_second_half, -a[N + i])
    
    # Calculate the initial score
    current_score = (prefix_sum[N] - prefix_sum[0]) - (prefix_sum[2 * N] - prefix_sum[N])
    
    # Variable to store the maximum score
    max_score = current_score
    
    # Iterate over the remaining elements
    for i in range(N, 2 * N):
        # Remove the element that will be moved from the first half to the second half
        element_to_move = heapq.heappop(min_heap_first_half)
        current_score -= element_to_move
        
        # Add the new element to the first half
        heapq.heappush(min_heap_first_half, a[i])
        current_score += a[i]
        
        # Remove the element that will be moved from the second half to the first half
        element_to_move = -heapq.heappop(max_heap_second_half)
        current_score += element_to_move
        
        # Add the new element to the second half
        heapq.heappush(max_heap_second_half, -a[i + N])
        current_score -= a[i + N]
        
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