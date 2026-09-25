import sys
from collections import Counter

def min_operations_to_equal_k(n, k, a):
    # Count the frequency of each number in the array
    freq = Counter(a)
    
    # If there's already a number that appears at least k times, no operations are needed
    if max(freq.values()) >= k:
        return 0
    
    # Calculate the minimum operations needed to make at least k numbers equal
    min_operations = float('inf')
    
    for target in range(1, max(a) + 1):
        operations = 0
        for num in a:
            # Calculate the number of divisions needed to make num equal to target
            if num != target:
                operations += (num - 1).bit_length() - (target - 1).bit_length()
        
        # Check if we can achieve at least k equal numbers with these operations
        if operations < min_operations:
            min_operations = operations
    
    return min_operations

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:]))

# Calculate and print the result
result = min_operations_to_equal_k(n, k, a)
print(result)