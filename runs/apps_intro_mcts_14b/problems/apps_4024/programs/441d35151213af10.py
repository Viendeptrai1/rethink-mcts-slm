import sys
from collections import defaultdict

def min_cost_to_obtain_set(n, k, s):
    if k > 2**n:
        return -1
    
    # Count the frequency of each character in the string
    freq = defaultdict(int)
    for char in s:
        freq[char] += 1
    
    # Calculate the cost for each unique character
    costs = []
    for char, count in freq.items():
        if count > 1:
            costs.append(count * (count - 1) // 2)
    
    # Sort costs in descending order
    costs.sort(reverse=True)
    
    # If we have enough unique subsequences, calculate the minimum cost
    if len(costs) >= k:
        return sum(costs[:k])
    else:
        return -1

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
s = data[2]

# Output the result
print(min_cost_to_obtain_set(n, k, s))