import heapq
import sys

def min_final_health(N, A):
    # Convert all healths to negative because heapq is a min-heap by default
    A = [-x for x in A]
    heapq.heapify(A)
    
    while len(A) > 1:
        # Pop the two strongest monsters (most negative numbers)
        a = -heapq.heappop(A)
        b = -heapq.heappop(A)
        
        # Attack the second strongest monster with the strongest monster
        if a > b:
            heapq.heappush(A, -(a - b))
    
    # Return the final health of the last monster
    return -A[0]

# Read input
input = sys.stdin.read
data = input().split()
N = int(data[0])
A = list(map(int, data[1:]))

# Print the result
print(min_final_health(N, A))