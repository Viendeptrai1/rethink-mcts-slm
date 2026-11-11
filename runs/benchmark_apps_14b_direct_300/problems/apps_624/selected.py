import sys
import heapq

def max_average_power(n, k, m, powers):
    # Calculate the initial sum of powers
    total_power = sum(powers)
    
    # Create a max-heap based on the negative values of powers
    max_heap = [-power for power in powers]
    heapq.heapify(max_heap)
    
    # Perform up to m operations
    for _ in range(m):
        # Get the superhero with the highest power (negated back to positive)
        max_power = -heapq.heappop(max_heap)
        
        # If we can increase this superhero's power, do so
        if k > 0:
            max_power += 1
            k -= 1
            total_power += 1
        
        # Push the updated power back into the heap
        heapq.heappush(max_heap, -max_power)
        
        # If we have used all allowed increases for this superhero, remove it
        if k == 0:
            n -= 1
            if n == 0:
                break
            k = 1
    
    # Calculate the maximum average power
    max_average = total_power / n
    
    return max_average

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
m = int(data[2])
powers = list(map(int, data[3:]))

# Calculate and print the result
result = max_average_power(n, k, m, powers)
print(f"{result:.20f}")