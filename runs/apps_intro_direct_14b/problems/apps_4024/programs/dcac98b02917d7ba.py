import sys
from collections import Counter

def min_cost_to_form_set(n, k, s):
    # Count the frequency of each character in the string
    freq = Counter(s)
    
    # Calculate the maximum number of unique subsequences we can form
    max_unique_subsequences = 1
    for count in freq.values():
        max_unique_subsequences *= (count + 1)
    
    # If the maximum number of unique subsequences is less than k, it's impossible
    if max_unique_subsequences < k:
        return -1
    
    # Calculate the minimum cost
    cost = 0
    for count in freq.values():
        cost += count * (count - 1) // 2
    
    return cost

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
s = data[2]

# Output the result
result = min_cost_to_form_set(n, k, s)
print(result)