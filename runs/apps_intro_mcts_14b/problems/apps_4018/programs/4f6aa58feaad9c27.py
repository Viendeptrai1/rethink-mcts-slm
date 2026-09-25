import sys

def min_cost_to_obtain_set(n, k, s):
    # Count the frequency of each character in the string
    freq = {}
    for char in s:
        if char in freq:
            freq[char] += 1
        else:
            freq[char] = 1
    
    # Calculate the maximum number of distinct subsequences
    max_subsequences = 1
    for count in freq.values():
        max_subsequences *= (count + 1)
    
    # If k is greater than the maximum number of distinct subsequences, return -1
    if k > max_subsequences:
        return -1
    
    # Calculate the minimum cost
    cost = 0
    current_subsequences = 1
    for count in sorted(freq.values(), reverse=True):
        while current_subsequences * (count + 1) <= k:
            current_subsequences *= (count + 1)
            cost += n - count
        if current_subsequences == k:
            break
    
    return cost

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
s = data[2]

# Output the result
print(min_cost_to_obtain_set(n, k, s))