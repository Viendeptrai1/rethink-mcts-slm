import sys
from collections import Counter

def min_cost_to_obtain_set(n, k, s):
    if k > 2**n:
        return -1
    
    # Count the frequency of each character in the string
    char_count = Counter(s)
    
    # Calculate the cost for each unique character
    costs = []
    for char, count in char_count.items():
        cost = n - count
        costs.append(cost)
    
    # Sort costs in ascending order
    costs.sort()
    
    # If k is greater than the number of unique subsequences, return -1
    if k > len(costs):
        return -1
    
    # Sum the k smallest costs
    total_cost = sum(costs[:k])
    
    return total_cost

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
s = data[2]

# Output the result
result = min_cost_to_obtain_set(n, k, s)
print(result)