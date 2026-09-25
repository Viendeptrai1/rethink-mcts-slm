import sys

def min_cost_to_obtain_set(n, k, s):
    # If k is greater than the number of possible subsequences, return -1
    if k > 2**n:
        return -1
    
    # Calculate the minimum cost
    cost = 0
    current_size = 1  # Start with the empty subsequence
    while current_size < k:
        # Double the size of the set by adding subsequences of length n - current_size
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
print(min_cost_to_obtain_set(n, k, s))