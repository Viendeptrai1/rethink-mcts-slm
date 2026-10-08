import sys
import bisect

def min_operations_to_increasing(n, k, a, b):
    if k == 0:
        # If no indices are fixed, we can change all elements freely
        return n - 1
    
    # Convert b to a set for O(1) lookups
    b_set = set(b)
    
    # Create a list of indices that are not in b
    free_indices = [i for i in range(n) if i + 1 not in b_set]
    
    # If there are fewer free indices than n-1, it's impossible to make the array increasing
    if len(free_indices) < n - 1:
        return -1
    
    # Initialize the result with the number of free indices minus (n-1)
    result = len(free_indices) - (n - 1)
    
    # Create a list of elements at free indices
    free_elements = [a[i] for i in free_indices]
    
    # Sort the free elements
    free_elements.sort()
    
    # Use a Fenwick Tree (Binary Indexed Tree) to count the number of elements less than a given value
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
    
    # Iterate through the sorted free elements and update the Fenwick Tree
    for element in free_elements:
        # Find the position where this element should be inserted to keep the array increasing
        pos = bisect.bisect_right(free_elements, element)
        
        # The number of elements less than the current element is the position minus one
        smaller_count = pos - 1
        
        # The number of elements greater than the current element is the total number of free elements minus the position
        larger_count = len(free_elements) - pos
        
        # Update the result with the minimum number of changes needed
        result = min(result, smaller_count + larger_count)
        
        # Update the Fenwick Tree with the current element
        update(pos, 1)
    
    return result

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
print(min_operations_to_increasing(n, k, a, b))