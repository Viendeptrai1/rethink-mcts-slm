def min_operations_to_increasing(n, k, a, b):
    # Convert b to a set for O(1) lookups
    b_set = set(b)
    
    # Create a list of indices where we need to make changes
    indices_to_change = []
    for i in range(1, n):
        if a[i] <= a[i - 1]:
            indices_to_change.append(i)
    
    # If there are no indices to change, return 0
    if not indices_to_change:
        return 0
    
    # If the number of indices to change is greater than the number of allowed operations, return -1
    if len(indices_to_change) > n - k:
        return -1
    
    # Calculate the minimum number of operations needed
    operations = 0
    for i in range(len(indices_to_change)):
        if indices_to_change[i] not in b_set:
            operations += 1
    
    return operations

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:n+2]))
if k > 0:
    b = list(map(int, data[n+2:n+k+2]))
else:
    b = []

# Output the result
print(min_operations_to_increasing(n, k, a, b))