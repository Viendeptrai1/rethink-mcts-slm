from itertools import permutations
from collections import defaultdict

def count_valid_orderings(names):
    MOD = 1_000_000_007
    
    # Create a dictionary to group names by their initial sequences
    groups = defaultdict(list)
    for name in names:
        for length in range(1, len(name) + 1):
            groups[name[:length]].append(name)
    
    # Calculate the factorial of n modulo MOD
    def factorial_mod(n):
        result = 1
        for i in range(2, n + 1):
            result = (result * i) % MOD
        return result
    
    # Calculate the number of valid orderings
    total_orderings = 1
    for group in groups.values():
        group_size = len(group)
        if group_size > 1:
            total_orderings = (total_orderings * factorial_mod(group_size)) % MOD
    
    return total_orderings

# Read input
import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
names = data[1:]

# Calculate and print the result
print(count_valid_orderings(names))