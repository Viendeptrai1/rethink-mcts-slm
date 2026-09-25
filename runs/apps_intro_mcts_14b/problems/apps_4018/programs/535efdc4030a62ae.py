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
    current_subsequences = 1
    for count in freq:
        if current_subsequences >= k:
            break
        # Calculate the number of new subsequences we can form with the current character
        new_subsequences = current_subsequences * count
        # If adding all new subsequences exceeds k, only add enough to reach k
        if current_subsequences + new_subsequences > k:
            additional_needed = k - current_subsequences
            cost += additional_needed * (n - current_subsequences)
            break
        cost += new_subsequences * (n - current_subsequences)
        current_subsequences += new_subsequences
    
    return cost

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
s = data[2]

# Output the result
result = min_cost_to_obtain_set(n, k, s)
print(result)