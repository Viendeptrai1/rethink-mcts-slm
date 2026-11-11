import sys
import bisect

def min_operations_to_increasing(n, k, a, b):
    if k == 0:
        # If no positions are fixed, we can freely change all elements
        return n - 1
    
    # Convert b to a set for O(1) lookups
    b_set = set(b)
    
    # Create a list of indices that are not fixed
    free_indices = [i for i in range(n) if i + 1 not in b_set]
    
    # If there are fewer than 2 free indices, it's impossible to make the array increasing
    if len(free_indices) < 2:
        return -1
    
    # Create a list of values at the free indices
    free_values = [a[i] for i in free_indices]
    
    # Sort the free values to determine the minimum number of changes needed
    sorted_free_values = sorted(free_values)
    
    # Use binary search to count the number of changes needed
    changes = 0
    for i in range(len(free_indices)):
        idx = bisect.bisect_left(sorted_free_values, free_values[i])
        if idx != i:
            changes += 1
    
    return changes

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:2+n]))
if k > 0:
    b = list(map(int, data[2+n:2+n+k]))
else:
    b = []

# Calculate and print the result
result = min_operations_to_increasing(n, k, a, b)
print(result)