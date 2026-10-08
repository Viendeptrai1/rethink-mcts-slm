def expected_score(n, k):
    # Create a memoization table to store results of subproblems
    memo = [[-1] * (k + 1) for _ in range(n + 1)]
    
    def dp(sides, rolls_left):
        # Base case: if no rolls left, the expected score is 0
        if rolls_left == 0:
            return 0
        # If already computed, return the stored result
        if memo[sides][rolls_left] != -1:
            return memo[sides][rolls_left]
        
        # Calculate the expected score for the current state
        max_expected = 0
        for i in range(1, sides + 1):
            if rolls_left == 1:
                # If only one roll left, take the maximum possible outcome
                max_expected = max(max_expected, i)
            else:
                # Otherwise, consider the expected value of continuing to roll
                max_expected = max(max_expected, (i + dp(sides, rolls_left - 1)) / sides)
        
        # Store the result in the memoization table
        memo[sides][rolls_left] = max_expected
        return max_expected
    
    # Start the dynamic programming from the full die and k rolls
    return dp(n, k)

# Read input from stdin
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])

# Calculate and print the expected score
print(expected_score(n, k))