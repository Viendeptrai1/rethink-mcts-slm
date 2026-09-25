import sys

def min_cost(n, k, s):
    unique_chars = len(set(s))
    if k > 2**unique_chars:
        return -1
    
    # Calculate the cost for each possible subsequence length
    costs = [0] * (n + 1)
    for i in range(1, n + 1):
        costs[i] = costs[i - 1] + (n - i)
    
    # Calculate the minimum cost to get k unique subsequences
    total_cost = 0
    current_subsequences = 0
    for i in range(n, 0, -1):
        if current_subsequences + 2**(n - i) >= k:
            additional_needed = k - current_subsequences
            total_cost += costs[i] * additional_needed
            break
        total_cost += costs[i]
        current_subsequences += 2**(n - i)
    
    return total_cost

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
s = data[2]

# Output the result
print(min_cost(n, k, s))