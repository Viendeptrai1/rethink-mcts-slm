import sys
from itertools import combinations

def min_cost_to_form_set(n, k, s):
    # Generate all possible subsequences
    subsequences = set()
    for i in range(1, n + 1):
        for comb in combinations(s, i):
            subsequences.add(''.join(comb))
    
    # If the number of unique subsequences is less than k, return -1
    if len(subsequences) < k:
        return -1
    
    # Calculate the cost for each subsequence
    costs = {}
    for subseq in subsequences:
        costs[subseq] = n - len(subseq)
    
    # Sort subsequences by their cost
    sorted_subsequences = sorted(subsequences, key=lambda x: costs[x])
    
    # Sum the costs of the first k subsequences
    total_cost = sum(costs[subseq] for subseq in sorted_subsequences[:k])
    
    return total_cost

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
s = data[2]

# Output the result
print(min_cost_to_form_set(n, k, s))