import sys
import bisect

def min_operations_to_increase(n, k, a, b):
    if k == 0:
        # If no elements are fixed, we can always sort the array in O(n log n)
        return n - len(set(a))
    
    # Convert b to a set for faster lookup
    b_set = set(b)
    
    # Create a list of indices that are not in b
    free_indices = [i for i in range(n) if i + 1 not in b_set]
    
    # Create a list of values at free indices
    free_values = [a[i] for i in free_indices]
    
    # Sort the free values
    free_values.sort()
    
    # Use a Fenwick Tree (Binary Indexed Tree) to count the number of elements less than or equal to a value
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
    
    # Initialize the Fenwick Tree with the sorted free values
    for value in free_values:
        update(value, 1)
    
    # Calculate the minimum number of operations needed
    operations = 0
    for i in range(n):
        if i + 1 in b_set:
            continue
        
        # Find the position where the current value should be inserted in the sorted free values
        pos = bisect.bisect_right(free_values, a[i])
        
        # The number of elements less than or equal to a[i] in the Fenwick Tree
        count_less_equal = query(a[i])
        
        # The number of elements greater than a[i] in the Fenwick Tree
        count_greater = len(free_values) - count_less_equal
        
        # If there are no elements greater than a[i], it's impossible to make the array increasing
        if count_greater == 0:
            return -1
        
        # Update the Fenwick Tree to reflect the removal of a[i]
        update(a[i], -1)
        
        # Find the smallest element greater than a[i] in the sorted free values
        next_value = free_values[pos]
        
        # Update the Fenwick Tree to reflect the insertion of next_value
        update(next_value, 1)
        
        # Increment the number of operations
        operations += 1
    
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

# Output the result
print(min_operations_to_increase(n, k, a, b))