def max_average_power(n, k, m, powers):
    from heapq import heappush, heappop

    # Calculate the initial sum of powers
    total_power = sum(powers)
    
    # Create a min-heap to track the smallest power values
    min_heap = []
    
    # Populate the heap with the negative of powers to simulate a max-heap
    for power in powers:
        heappush(min_heap, power)
    
    # Perform operations to maximize the average power
    for _ in range(m):
        # Get the smallest power from the heap
        smallest_power = heappop(min_heap)
        
        # Increase the smallest power by 1
        smallest_power += 1
        
        # Push the increased power back into the heap
        heappush(min_heap, smallest_power)
    
    # Calculate the maximum possible average power
    max_average = sum(min_heap) / n
    
    return max_average

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
m = int(data[2])
powers = list(map(int, data[3:3+n]))

# Get the result and print it
result = max_average_power(n, k, m, powers)
print(f"{result:.15f}")