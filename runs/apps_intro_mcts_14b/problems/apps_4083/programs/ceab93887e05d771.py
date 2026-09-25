import sys
from collections import Counter

def min_operations_to_k_equal(n, k, a):
    # Count the frequency of each number in the array
    freq = Counter(a)
    
    # If the most frequent number already appears at least k times, no operations are needed
    if max(freq.values()) >= k:
        return 0
    
    # Calculate the minimum operations needed to make at least k numbers equal
    min_operations = float('inf')
    
    # Try making all numbers equal to each unique number in the array
    for num in freq:
        operations = 0
        for value in a:
            # Calculate the number of operations needed to transform value to num
            operations += bin(value).count('1') - bin(num).count('1')
        # Update the minimum operations if the current number of operations is less
        min_operations = min(min_operations, operations)
    
    return min_operations

# Read input from standard input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:]))

# Calculate and print the result
result = min_operations_to_k_equal(n, k, a)
print(result)