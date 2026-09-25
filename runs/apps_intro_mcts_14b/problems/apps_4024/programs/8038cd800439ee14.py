import sys
from itertools import combinations

def min_cost_to_create_set(n, k, s):
    # Check if it's possible to create a set S of size k
    if k > 2**n:
        return -1
    
    # Generate all unique subsequences
    subsequences = set()
    for r in range(1, n + 1):
        for comb in combinations(s, r):
            subsequences.add(''.join(comb))
    
    # If the number of unique subsequences is less than k, return -1
    if len(subsequences) < k:
        return -1
    
    # Calculate the cost for each subsequence
    costs = [n - len(subseq) for subseq in subsequences]
    
    # Sort costs in ascending order
    costs.sort()
    
    # Sum the first k costs
    return sum(costs[:k])

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
s = data[2]

# Output the result
print(min_cost_to_create_set(n, k, s))