import sys

def min_cost_to_obtain_set(n, k, s):
    # Calculate the maximum number of unique subsequences we can get
    max_unique_subsequences = 2 ** n
    
    # If k is greater than the maximum number of unique subsequences, it's impossible
    if k > max_unique_subsequences:
        return -1
    
    # The minimum cost to obtain k unique subsequences is the sum of the first (k-1) natural numbers
    # because the cost of adding each new subsequence is the number of characters deleted
    # which is n - |t|, and the shortest subsequence we can add is of length 1 (a single character)
    # so the cost for the first subsequence is 0, for the second it's 1, and so on.
    min_cost = (k - 1) * k // 2
    
    return min_cost

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
s = data[2]

# Calculate and print the result
result = min_cost_to_obtain_set(n, k, s)
print(result)