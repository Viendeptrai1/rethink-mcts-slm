import sys
import bisect

def min_operations_to_increasing(n, k, a, b):
    if k == 0:
        # If no elements are fixed, we can always sort the array
        return n - 1 if a != sorted(a) else 0
    
    # Convert b to a set for O(1) lookups
    b_set = set(b)
    
    # Create a list of indices that are not in b
    free_indices = [i for i in range(n) if i + 1 not in b_set]
    
    # Create a list of values at free indices
    free_values = [a[i] for i in free_indices]
    
    # Sort the free values
    sorted_free_values = sorted(free_values)
    
    # Use a Fenwick Tree to count inversions
    fenwick_tree = [0] * (n + 1)
    
    def update(index, value):
        while index <= n:
            fenwick_tree[index] += value
            index += index & -index
    
    def query(index):
        result = 0
        while index > 0:
            result += fenwick_tree[index]
            index -= index & -index
        return result
    
    # Count the number of operations needed
    operations = 0
    for i in range(len(free_indices)):
        # Find the position where the current value should be inserted
        pos = bisect.bisect_left(sorted_free_values, free_values[i])
        
        # The number of elements greater than free_values[i] to the left
        greater_count = i - pos
        
        # The number of elements less than free_values[i] to the right
        lesser_count = len(free_indices) - i - 1 - (len(sorted_free_values) - 1 - pos)
        
        # Update the Fenwick Tree
        update(pos + 1, 1)
        
        # Add the number of operations needed
        operations += greater_count + lesser_count
    
    # Check if the array can be made increasing
    if operations > len(free_indices) - 1:
        return -1
    
    return operations

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:2+n]))
if k != 0:
    b = list(map(int, data[2+n:2+n+k]))
else:
    b = []

# Calculate and print the result
result = min_operations_to_increasing(n, k, a, b)
print(result)