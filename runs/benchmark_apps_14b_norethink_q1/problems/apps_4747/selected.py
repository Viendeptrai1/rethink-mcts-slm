def expected_score(n, k):
    # Create a memoization table to store results of subproblems
    memo = [[-1] * (k + 1) for _ in range(n + 1)]
    
    def E(n, k):
        # Base case: if there's only one roll left, the expected value is the average of all outcomes
        if k == 1:
            return (1 + n) / 2
        
        # If the result is already computed, return it
        if memo[n][k] != -1:
            return memo[n][k]
        
        # Calculate the expected score for k rolls
        expected = 0
        for i in range(1, n + 1):
            expected += max(i, E(n, k - 1))
        
        # Store the result in the memoization table
        memo[n][k] = expected / n
        return memo[n][k]
    
    # Return the expected score for n-sided die with k rolls
    return E(n, k)

# Read input from stdin
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])

# Print the result
print(expected_score(n, k))