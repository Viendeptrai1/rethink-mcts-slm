import sys

def min_cost(n, k, s):
    unique_chars = len(set(s))
    if k > 2**unique_chars:
        return -1
    
    # Calculate the minimum cost
    cost = 0
    current_size = 1
    while current_size < k:
        cost += n - current_size
        current_size *= 2
    
    return cost

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
s = data[2]

# Output the result
print(min_cost(n, k, s))