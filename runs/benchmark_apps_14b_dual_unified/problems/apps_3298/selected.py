MOD = 10**9 + 9

def count_entirely_unsorted_sequences(n, a):
    from collections import Counter
    
    # Count the frequency of each element
    freq = Counter(a)
    
    # Sort the unique elements
    unique_elements = sorted(freq.keys())
    
    # Number of unique elements
    m = len(unique_elements)
    
    # dp[i][j] will store the number of ways to arrange the first i unique elements
    # such that the last element appears exactly j times
    dp = [[0] * (freq[unique_elements[i]] + 1) for i in range(m)]
    
    # Base case: There's one way to arrange zero elements
    dp[0][0] = 1
    
    for i in range(1, m):
        for j in range(freq[unique_elements[i]] + 1):
            # Case 1: Don't include the current element at all
            dp[i][j] = dp[i-1][j]
            
            # Case 2: Include the current element k times (1 <= k <= freq[unique_elements[i]])
            for k in range(1, min(j + 1, freq[unique_elements[i]] + 1)):
                dp[i][j] = (dp[i][j] + dp[i-1][j-k]) % MOD
    
    # Sum up all ways to arrange all unique elements
    total_ways = sum(dp[m-1]) % MOD
    
    # Subtract the cases where at least one element is sorted
    # This is equivalent to subtracting the number of ways to arrange the elements
    # such that at least one element appears more than once consecutively
    sorted_ways = 0
    
    for i in range(1, m):
        for j in range(1, freq[unique_elements[i]] + 1):
            sorted_ways = (sorted_ways + dp[i-1][j-1]) % MOD
    
    # The result is the total ways minus the sorted ways
    result = (total_ways - sorted_ways + MOD) % MOD
    
    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Print the result
print(count_entirely_unsorted_sequences(n, a))