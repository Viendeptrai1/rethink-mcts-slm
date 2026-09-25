import sys
from collections import Counter

def min_operations_to_equal_k(n, k, a):
    # Count the frequency of each number in the array
    count = Counter(a)
    
    # Find the most frequent number
    max_freq = max(count.values())
    
    # If the most frequent number already appears at least k times, no operations are needed
    if max_freq >= k:
        return 0
    
    # Calculate the minimum number of operations needed
    operations = float('inf')
    for num in count:
        total_operations = 0
        for other_num in count:
            if num != other_num:
                # Calculate the number of operations needed to make other_num equal to num
                total_operations += count[other_num] * (num.bit_length() - other_num.bit_length())
        # Update the minimum operations if the current total is smaller
        operations = min(operations, total_operations)
    
    return operations

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:]))

# Calculate and print the result
print(min_operations_to_equal_k(n, k, a))