import sys
from collections import defaultdict

def min_cost_to_obtain_set(n, k, s):
    # Generate all unique subsequences
    subsequences = defaultdict(int)
    
    # Use bit manipulation to generate all subsequences
    for mask in range(1 << n):
        subseq = ''.join(s[j] for j in range(n) if mask & (1 << j))
        subsequences[subseq] += 1
    
    # Sort subsequences by length
    sorted_subsequences = sorted(subsequences.keys(), key=len)
    
    # Initialize DP table
    dp = [float('inf')] * (k + 1)
    dp[0] = 0
    
    # Fill DP table
    for subseq in sorted_subsequences:
        cost = n - len(subseq)
        for i in range(k, 0, -1):
            dp[i] = min(dp[i], dp[i - 1] + cost)
    
    return dp[k] if dp[k] != float('inf') else -1

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
s = data[2]

# Output the result
result = min_cost_to_obtain_set(n, k, s)
print(result)