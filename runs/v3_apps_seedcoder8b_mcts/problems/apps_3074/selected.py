def count_valid_subsets(N, S):
    MOD = 10**9 + 7
    
    # dp[i][j] will store the number of ways to form a number with remainder j
    # when considering the first i digits of S
    dp = [[0] * 3 for _ in range(N + 1)]
    dp[0][0] = 1  # Base case: one way to form 0 remainder with 0 digits
    
    for i in range(1, N + 1):
        digit = int(S[i - 1])
        for j in range(3):
            # Carry forward the count from the previous state
            dp[i][j] = dp[i - 1][j]
            # Add the current digit to form new remainders
            dp[i][(j * 10 + digit) % 3] = (dp[i][(j * 10 + digit) % 3] + dp[i - 1][j]) % MOD
    
    # We want subsets that form numbers divisible by 3, excluding the empty subset
    return (dp[N][0] - 1) % MOD

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    S = data[1]
    
    result = count_valid_subsets(N, S)
    print(result)

if __name__ == "__main__":
    main()