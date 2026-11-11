import sys
import heapq

def max_average_power(n, k, m, powers):
    # Calculate the sum of all powers
    total_power = sum(powers)
    
    # Create a max-heap based on the difference between k and the current power
    max_heap = []
    for power in powers:
        heapq.heappush(max_heap, (-min(k, power), power))
    
    # Perform up to m operations
    for _ in range(m):
        if len(max_heap) < 2:
            break
        
        # Get the superhero with the highest potential increase
        diff, power = heapq.heappop(max_heap)
        diff = -diff
        
        # Increase the power of this superhero
        new_power = power + min(diff, m)
        total_power += min(diff, m)
        m -= min(diff, m)
        
        # Push the updated superhero back into the heap
        new_diff = min(k, new_power) - new_power
        heapq.heappush(max_heap, (-new_diff, new_power))
    
    # Calculate the maximum average power
    max_avg_power = total_power / len(max_heap)
    return max_avg_power

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
m = int(data[2])
powers = list(map(int, data[3:]))

# Output the result
print(max_average_power(n, k, m, powers))