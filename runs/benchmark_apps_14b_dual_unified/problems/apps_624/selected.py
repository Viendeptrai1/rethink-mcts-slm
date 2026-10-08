import sys
import heapq

def max_average_power(n, k, m, powers):
    # Sort the powers in ascending order
    powers.sort()
    
    # Calculate the total sum of powers
    total_sum = sum(powers)
    
    # Use a max-heap to keep track of the potential increases
    max_heap = []
    for i in range(n):
        heapq.heappush(max_heap, (-powers[i], i))
    
    # Perform up to m operations
    for _ in range(m):
        if not max_heap:
            break
        
        # Get the superhero with the highest potential increase
        power, index = heapq.heappop(max_heap)
        power = -power
        
        # If we can still increase this superhero's power
        if power < powers[index] + k:
            # Increase the power
            new_power = min(power + 1, powers[index] + k)
            total_sum += new_power - powers[index]
            powers[index] = new_power
            heapq.heappush(max_heap, (-new_power, index))
        else:
            # Remove the superhero if we can't increase it further
            total_sum -= powers[index]
            n -= 1
    
    # Calculate the maximum average power
    if n == 0:
        return 0.0
    else:
        return total_sum / n

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