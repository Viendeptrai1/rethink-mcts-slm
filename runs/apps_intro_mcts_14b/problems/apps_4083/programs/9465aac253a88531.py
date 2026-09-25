import sys
from collections import Counter

def min_operations_to_equal_numbers(n, k, a):
    # Count the frequency of each number in the array
    freq = Counter(a)
    
    # Sort the frequencies in descending order
    sorted_freq = sorted(freq.values(), reverse=True)
    
    # Calculate the minimum number of operations needed
    operations = 0
    for count in sorted_freq:
        if k <= 0:
            break
        operations += count * (2 ** (len(sorted_freq) - 1))
        k -= count
    
    return operations

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:]))

# Calculate and print the result
result = min_operations_to_equal_numbers(n, k, a)
print(result)