import sys

def min_cost_to_form_set(n, k, s):
    if k > 2**n:
        return -1
    
    # Calculate the frequency of each character in the string
    freq = [0] * 26
    for char in s:
        freq[ord(char) - ord('a')] += 1
    
    # Sort frequencies in descending order
    freq.sort(reverse=True)
    
    # Calculate the maximum number of unique subsequences we can form
    max_unique_subsequences = 1
    for f in freq:
        max_unique_subsequences *= (f + 1)
    
    if k > max_unique_subsequences:
        return -1
    
    # Calculate the minimum cost
    cost = 0
    current_subsequences = 1
    for i in range(26):
        if current_subsequences >= k:
            break
        current_subsequences *= (freq[i] + 1)
        if current_subsequences >= k:
            additional_needed = k - (current_subsequences // (freq[i] + 1))
            cost += additional_needed * (n - i)
            break
        cost += freq[i] * (n - i)
    
    return cost

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
s = data[2]

# Output the result
print(min_cost_to_form_set(n, k, s))