import sys
from itertools import combinations

def min_cost_to_form_set(n, k, s):
    if k > 2**n:
        return -1
    
    # Generate all possible subsequences
    subsequences = []
    for i in range(1, n + 1):
        for comb in combinations(s, i):
            subsequences.append(''.join(comb))
    
    # Sort subsequences by their length
    subsequences.sort(key=len)
    
    # Use a set to keep track of unique subsequences
    unique_subsequences = set()
    cost = 0
    
    for subseq in subsequences:
        if len(unique_subsequences) == k:
            break
        if subseq not in unique_subsequences:
            unique_subsequences.add(subseq)
            cost += n - len(subseq)
    
    if len(unique_subsequences) < k:
        return -1
    
    return cost

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
s = data[2]

# Output the result
print(min_cost_to_form_set(n, k, s))