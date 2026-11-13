import heapq
import sys

def min_final_health(N, A):
    # Convert A to a max heap by negating the values
    hp = [-x for x in A]
    heapq.heapify(hp)
    
    while len(hp) > 1:
        # Pop two largest elements (smallest in magnitude due to negation)
        a = -heapq.heappop(hp)
        b = -heapq.heappop(hp)
        
        # Calculate the new health after attack
        if a > b:
            heapq.heappush(hp, -(a - b))
    
    # The remaining element is the minimum possible final health
    return -hp[0]

# Read input from stdin
input = sys.stdin.read
data = input().split()
N = int(data[0])
A = list(map(int, data[1:]))

# Print the result
print(min_final_health(N, A))