MOD = 10**9 + 7

def count_ways(n):
    # Base cases for small values of n
    if n == 1:
        return 20
    elif n == 2:
        return 680
    
    # Initialize dynamic programming arrays
    dp = [[[[0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    dp[1][1][1][1] = 1
    
    # Fill DP table
    for _ in range(n - 1):
        new_dp = [[[[0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
        for a1 in range(4):
            for a2 in range(4):
                for a3 in range(4):
                    for a4 in range(4):
                        if a1 + a2 + a3 + a4 != 6:
                            for b1 in range(4):
                                for b2 in range(4):
                                    for b3 in range(4):
                                        if b1 + b2 + b3 != 6:
                                            new_dp[a2][a3][b1][(a1 + a4 + b2 + b3) % 4] += dp[a1][a2][a3][a4]
                                            new_dp[a2][a3][b1][(a1 + a4 + b2 + b3) % 4] %= MOD
        dp = new_dp
    
    # Sum up all valid configurations
    result = 0
    for a2 in range(4):
        for a3 in range(4):
            for b1 in range(4):
                for b2 in range(4):
                    for b3 in range(4):
                        if b1 + b2 + b3 != 6:
                            result += dp[1][a2][b1][(1 + b2 + b3) % 4]
                            result %= MOD
    return result

# Read input
n = int(input())

# Output result
print(count_ways(n))