import sys
from collections import Counter

def min_operations_to_equalize(n, k, a):
    # Count the frequency of each number in the array
    count = Counter(a)
    
    # Sort the frequencies in descending order
    freqs = sorted(count.values(), reverse=True)
    
    # Calculate the minimum number of operations needed
    operations = 0
    for i in range(k):
        if i < len(freqs):
            operations += sum(count[a] - freqs[i] for a in count if count[a] > freqs[i])
        else:
            operations += sum(count[a] for a in count)
    
    return operations

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:]))

# Calculate and print the result
result = min_operations_to_equalize(n, k, a)
print(result)