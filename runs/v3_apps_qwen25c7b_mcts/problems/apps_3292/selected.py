from collections import defaultdict
import math

MOD = 1_000_000_007

def count_valid_orderings(names):
    n = len(names)
    
    # Group names by their starting sequence
    groups = defaultdict(list)
    for name in names:
        groups[name[0]].append(name)
    
    # Calculate factorial modulo MOD
    def factorial(x):
        result = 1
        for i in range(2, x + 1):
            result = (result * i) % MOD
        return result
    
    # Calculate the product of factorials of group sizes modulo MOD
    total_permutations = 1
    for group in groups.values():
        total_permutations = (total_permutations * factorial(len(group))) % MOD
    
    # Calculate the number of ways to arrange the groups
    num_groups = len(groups)
    group_arrangements = factorial(num_groups)
    
    # Total number of valid orderings
    return (total_permutations * group_arrangements) % MOD

# Read input
n = int(input().strip())
names = [input().strip() for _ in range(n)]

# Output the result
print(count_valid_orderings(names))