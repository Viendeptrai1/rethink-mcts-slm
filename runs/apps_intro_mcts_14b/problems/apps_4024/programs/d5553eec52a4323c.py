import sys
from itertools import combinations

def min_cost_to_form_set(n, k, s):
    if k > 2**n:
        return -1
    
    # Generate all possible subsequences and calculate their costs
    subsequences = []
    for r in range(1, n + 1):
        for comb in combinations(range(n), r):
            subseq = ''.join(s[i] for i in comb)
            subsequences.append((subseq, n - len(subseq)))
    
    # Sort subsequences by cost and then by lexicographical order
    subsequences.sort(key=lambda x: (x[1], x[0]))
    
    # Use a set to keep track of unique subsequences
    unique_subsequences = set()
    total_cost = 0
    
    for subseq, cost in subsequences:
        if len(unique_subsequences) == k:
            break
        if subseq not in unique_subsequences:
            unique_subsequences.add(subseq)
            total_cost += cost
    
    if len(unique_subsequences) < k:
        return -1
    
    return total_cost

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
s = data[2]

# Output the result
print(min_cost_to_form_set(n, k, s))