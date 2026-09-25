import sys

def min_cost_to_form_set(n, k, s):
    # If k is greater than the number of possible subsequences, return -1
    if k > 2**n:
        return -1
    
    # Calculate the minimum cost
    cost = 0
    current_subsequences = 1  # Start with the empty subsequence
    i = 0
    
    while current_subsequences < k:
        # Each new character can double the number of subsequences
        current_subsequences *= 2
        cost += n - i
        i += 1
    
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