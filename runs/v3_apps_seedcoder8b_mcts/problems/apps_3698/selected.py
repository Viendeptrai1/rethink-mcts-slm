MOD = 10**9 + 7

def count_special_numbers(n_bin, k):
    n = int(n_bin, 2)
    max_bits = len(n_bin)
    
    # dp[i][j] will store the number of ways to reduce i to 1 in j operations
    dp = [[0] * (k + 1) for _ in range(max_bits + 1)]
    dp[1][0] = 1  # Base case: 1 can be reduced to 1 in 0 operations
    
    # Fill the dp table
    for bits in range(1, max_bits + 1):
        for ops in range(k + 1):
            # Carry over the previous state
            dp[bits][ops] = dp[bits - 1][ops]
            if ops > 0:
                # Add the number of ways to reach this state by setting the current bit
                dp[bits][ops] = (dp[bits][ops] + dp[bits - 1][ops - 1]) % MOD
    
    # Count special numbers not greater than n
    def count_upto(x):
        if x == 0:
            return 0
        bits = x.bit_length()
        count = 0
        ops_used = 0
        
        for b in range(bits, 0, -1):
            if x & (1 << (b - 1)):
                # If the b-th bit is set
                count = (count + dp[b][k - ops_used]) % MOD
                ops_used += 1
                if ops_used > k:
                    break
        
        # Check if the number itself is special
        if ops_used == k:
            count = (count + 1) % MOD
        
        return count
    
    return count_upto(n)

# Read input
n_bin = input().strip()
k = int(input().strip())

# Output the result
print(count_special_numbers(n_bin, k))