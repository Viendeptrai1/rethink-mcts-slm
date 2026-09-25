import sys
from collections import Counter

def min_cost_to_obtain_set(n, k, s):
    if k > 2**n:
        return -1
    
    # Count the frequency of each character in the string
    char_count = Counter(s)
    
    # Calculate the maximum number of unique subsequences we can form
    max_unique_subsequences = 1
    for count in char_count.values():
        max_unique_subsequences *= (count + 1)
    
    if k > max_unique_subsequences:
        return -1
    
    # Calculate the minimum cost
    cost = 0
    for i in range(1, k + 1):
        cost += n - i + 1
    
    return cost

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
s = data[2]

# Output the result
print(min_cost_to_obtain_set(n, k, s))