import sys
from collections import Counter

def min_operations_to_equalize(n, k, a):
    # Count the frequency of each number in the array
    count = Counter(a)
    
    # Find the maximum frequency of any number
    max_freq = max(count.values())
    
    # If the maximum frequency is already at least k, no operations are needed
    if max_freq >= k:
        return 0
    
    # Calculate the number of operations needed to increase the frequency of the most frequent number to k
    operations = 0
    for num, freq in count.items():
        if freq < k:
            # Calculate how many more occurrences we need
            needed = k - freq
            # Calculate the number of operations needed to get these occurrences
            # Each operation halves the number, so we need to find the smallest power of 2 greater than or equal to num
            # This is equivalent to finding the ceiling of log2(num)
            operations += needed * (num.bit_length() - 1)
    
    return operations

# Read input from standard input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:]))

# Calculate and print the result
result = min_operations_to_equalize(n, k, a)
print(result)