import sys

def min_cost_to_obtain_set(n, k, s):
    # Calculate the maximum number of unique subsequences we can form
    max_subsequences = 2 ** n
    
    # If k is greater than the maximum number of unique subsequences, it's impossible
    if k > max_subsequences:
        return -1
    
    # The cost to form k unique subsequences is simply the sum of the first (n-1) natural numbers
    # because each new subsequence can be formed by removing one character from the previous one.
    # This is equivalent to the sum of the series: (n-1) + (n-2) + ... + 1
    cost = (n - 1) * n // 2
    
    return cost

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
s = data[2]

# Output the result
print(min_cost_to_obtain_set(n, k, s))