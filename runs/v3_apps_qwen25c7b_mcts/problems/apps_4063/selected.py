from collections import Counter

def count_equal_divisions(N, difficulties):
    # Count the frequency of each difficulty level
    freq = Counter(difficulties)
    
    # Create a prefix sum array where prefix_sum[i] is the number of problems with difficulty <= i
    prefix_sum = [0] * (max(difficulties) + 1)
    for i in range(1, len(prefix_sum)):
        prefix_sum[i] = prefix_sum[i - 1] + freq[i]
    
    # Initialize counters for the number of valid divisions
    valid_divisions = 0
    
    # Iterate over possible values of K
    for K in range(1, max(difficulties) + 1):
        arcs_count = prefix_sum[-1] - prefix_sum[K - 1]
        abcs_count = prefix_sum[K - 1]
        if arcs_count == abcs_count:
            valid_divisions += 1
    
    return valid_divisions

# Read input
import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
difficulties = list(map(int, data[1:]))

# Calculate and print the result
result = count_equal_divisions(N, difficulties)
print(result)