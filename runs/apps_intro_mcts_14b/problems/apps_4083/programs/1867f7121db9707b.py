import sys
from collections import Counter

def min_operations_to_equal_numbers(n, k, a):
    # Count the frequency of each number in the array
    freq = Counter(a)
    
    # Find the maximum frequency
    max_freq = max(freq.values())
    
    # If the maximum frequency is already at least k, no operations are needed
    if max_freq >= k:
        return 0
    
    # Calculate the minimum number of operations needed
    operations = float('inf')
    for num, count in freq.items():
        # Calculate the number of operations needed to make all numbers equal to num
        current_operations = 0
        for value in a:
            if value != num:
                # Calculate the number of divisions needed to make value equal to num
                current_operations += (value - 1).bit_length() - (num - 1).bit_length()
        
        # Update the minimum operations if the current one is smaller
        operations = min(operations, current_operations)
    
    return operations

# Read input from standard input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:]))

# Calculate and print the result
result = min_operations_to_equal_numbers(n, k, a)
print(result)