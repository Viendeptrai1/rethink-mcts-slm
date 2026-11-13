from collections import defaultdict
from math import factorial

MOD = 1_000_000_007

def count_valid_orderings(names):
    # Group names by their initial sequences
    groups = defaultdict(list)
    for name in names:
        groups[name[0]].append(name)
    
    # Calculate the number of ways to arrange each group
    group_counts = [factorial(len(group)) for group in groups.values()]
    
    # Multiply the counts together to get the total number of valid orderings
    result = 1
    for count in group_counts:
        result = (result * count) % MOD
    
    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Number of names
N = int(data[0])

# List of names
names = data[1:]

# Output the result
print(count_valid_orderings(names))