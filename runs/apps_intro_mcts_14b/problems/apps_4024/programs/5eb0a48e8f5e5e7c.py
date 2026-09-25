import sys
from itertools import combinations

def min_cost_to_obtain_set(n, k, s):
    # Generate all unique subsequences
    subsequences = set()
    for r in range(1, n + 1):
        for comb in combinations(s, r):
            subsequences.add(''.join(comb))
    
    # If the number of unique subsequences is less than k, return -1
    if len(subsequences) < k:
        return -1
    
    # Sort subsequences by their cost (n - length)
    subsequences = sorted(subsequences, key=lambda x: n - len(x))
    
    # Select the first k subsequences
    selected_subsequences = subsequences[:k]
    
    # Calculate the total cost
    total_cost = sum(n - len(subseq) for subseq in selected_subsequences)
    
    return total_cost

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
s = data[2]

# Output the result
print(min_cost_to_obtain_set(n, k, s))