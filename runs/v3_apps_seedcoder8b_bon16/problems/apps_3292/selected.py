from collections import defaultdict
from math import factorial

MOD = 1000000007

def count_ranking_lists(names):
    # Sort names lexicographically
    names.sort()
    
    # Group names by their initial sequence
    groups = defaultdict(list)
    for name in names:
        for i in range(1, len(name) + 1):
            groups[name[:i]].append(name)
    
    # Count valid orderings
    def count_orderings(group):
        n = len(group)
        return factorial(n) * pow(n, n - 1, MOD) % MOD
    
    result = 1
    for group in groups.values():
        result = (result * count_orderings(group)) % MOD
    
    return result

# Read input
N = int(input())
names = [input().strip() for _ in range(N)]

# Calculate and print result
print(count_ranking_lists(names))