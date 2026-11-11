import sys
import heapq

def max_average_power(n, k, m, powers):
    # Calculate the total sum of powers
    total_sum = sum(powers)
    
    # Create a max-heap based on the negative values of powers
    max_heap = [-power for power in powers]
    heapq.heapify(max_heap)
    
    # Perform up to m operations
    for _ in range(m):
        # Get the current maximum power (negated back to positive)
        max_power = -heapq.heappop(max_heap)
        
        # If we can increase this power without exceeding k operations
        if k > 0:
            # Increase the power by 1
            max_power += 1
            # Decrease the allowed operations for this power
            k -= 1
            # Push the updated power back into the heap (negated)
            heapq.heappush(max_heap, -max_power)
        else:
            # If we can't increase this power, break out of the loop
            break
    
    # Calculate the new total sum after operations
    new_total_sum = total_sum + (m - k)
    
    # Calculate the new average power
    new_average_power = new_total_sum / n
    
    return new_average_power

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