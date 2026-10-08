import sys
from collections import defaultdict

def largest_k_multiple_free_subset(n, k, a):
    # Group numbers by their remainder when divided by k
    remainder_groups = defaultdict(list)
    for num in a:
        remainder_groups[num % k].append(num)
    
    max_size = 0
    
    # For each remainder group, sort the numbers and select every k-th element
    for group in remainder_groups.values():
        group.sort()
        # Select every k-th element starting from the smallest
        selected_count = len(group) // k + (1 if len(group) % k != 0 else 0)
        max_size += selected_count
    
    return max_size

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:]))

# Calculate and print the result
print(largest_k_multiple_free_subset(n, k, a))