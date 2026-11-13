def count_valid_subsets(N, S):
    MOD = 10**9 + 7
    
    # Convert string S to a list of integers
    digits = [int(d) for d in S]
    
    # Initialize dp array
    dp = [0] * 3
    dp[0] = 1  # Empty subset is always valid (divisible by 3)
    
    total_sum = 0
    
    for digit in digits:
        # Update total sum
        total_sum = (total_sum + digit) % 3
        
        # Calculate new dp values
        new_dp = [0] * 3
        for remainder in range(3):
            new_dp[remainder] = dp[remainder]
            new_dp[(remainder - digit) % 3] = (new_dp[(remainder - digit) % 3] + dp[remainder]) % MOD
        
        dp = new_dp
    
    # Subtract 1 to exclude the empty subset
    return (dp[0] - 1) % MOD

# Read input
N = int(input())
S = input().strip()

# Compute and print result
result = count_valid_subsets(N, S)
print(result)