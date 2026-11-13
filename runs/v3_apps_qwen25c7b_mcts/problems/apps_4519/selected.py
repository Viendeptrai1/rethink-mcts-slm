def min_lexicographical_string(n, k, s):
    count = [0] * 2
    misplaced = [0] * 2
    
    # Count misplaced '0's and '1's
    for i in range(n):
        if s[i] != str(i % 2):
            misplaced[int(s[i])] += 1
    
    # Calculate the minimum swaps needed to sort the string
    swaps_needed = max(misplaced)
    
    # If we have enough swaps, return the sorted string
    if swaps_needed <= k:
        return ''.join(sorted(s))
    
    # Otherwise, return the original string
    return s

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Process each test case
results = []
index = 0
for _ in range(int(data[index])):
    index += 1
    n = int(data[index])
    k = int(data[index + 1])
    s = data[index + 2]
    results.append(min_lexicographical_string(n, k, s))

# Print results
print('\n'.join(results))