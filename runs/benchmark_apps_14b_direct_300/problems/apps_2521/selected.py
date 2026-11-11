import sys
import heapq

def max_score(N, a):
    # Split the array into three parts
    part1 = a[:N]
    part2 = a[N:2*N]
    part3 = a[2*N:]
    
    # Max-heap for the first half and min-heap for the second half
    max_heap = []
    min_heap = []
    
    # Calculate the initial score with the first N elements in the first half
    first_half_sum = sum(part1)
    second_half_sum = sum(part2)
    current_score = first_half_sum - second_half_sum
    
    # Push all elements of part2 into the min-heap
    for num in part2:
        heapq.heappush(min_heap, num)
    
    # Push all elements of part1 into the max-heap
    for num in part1:
        heapq.heappush(max_heap, -num)
    
    # Try to improve the score by swapping elements between the two halves
    for num in part3:
        if num > -max_heap[0]:
            # Swap the largest element in the first half with the current number
            first_half_sum += num + heapq.heappop(max_heap)
            heapq.heappush(max_heap, -num)
            
            # Swap the smallest element in the second half with the smallest element in the max-heap
            second_half_sum -= heapq.heappop(min_heap)
            heapq.heappush(min_heap, -heapq.heappop(max_heap))
            heapq.heappush(max_heap, -min_heap[0])
            heapq.heappop(min_heap)
        
        current_score = max(current_score, first_half_sum - second_half_sum)
    
    return current_score

# Read input
input = sys.stdin.read
data = input().split()
N = int(data[0])
a = list(map(int, data[1:]))

# Print the result
print(max_score(N, a))