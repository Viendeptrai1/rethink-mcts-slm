import sys

def min_cost_to_obtain_set(n, k, s):
    # Count the frequency of each character in the string
    freq = [0] * 26
    for char in s:
        freq[ord(char) - ord('a')] += 1
    
    # Calculate the maximum number of unique subsequences we can form
    max_subsequences = 1
    for count in freq:
        max_subsequences *= (count + 1)
    
    # If k is greater than the maximum number of unique subsequences, return -1
    if k > max_subsequences:
        return -1
    
    # Calculate the minimum cost
    cost = 0
    for count in freq:
        cost += count * (k - 1)
    
    return cost

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
s = data[2]

# Output the result
print(min_cost_to_obtain_set(n, k, s))