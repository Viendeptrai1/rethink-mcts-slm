def count_regular_bracket_sequences(n, s):
    MOD = 1000000007
    m = len(s)
    
    # dp[i][j] will store the number of ways to form a valid sequence of length i+j
    # with j more '(' than ')'
    dp = [[0] * (n + 1) for _ in range(2 * n + 1)]
    dp[0][0] = 1  # Base case: one way to form an empty sequence
    
    for i in range(1, 2 * n + 1):
        for j in range(n + 1):
            if j > 0:
                dp[i][j] = dp[i - 1][j - 1]  # Add '('
            if j < n:
                dp[i][j] = (dp[i][j] + dp[i - 1][j + 1]) % MOD  # Add ')'
    
    # Now, we need to count the number of valid sequences of length 2n that contain s
    total_ways = dp[2 * n][0]  # Total ways to form a sequence of length 2n
    invalid_ways = 0
    
    # We will subtract the number of invalid sequences
    for i in range(2 * n - m + 1):
        # Check if s can be a substring starting at position i
        if is_valid_subsequence(s, i, n):
            invalid_ways = (invalid_ways + dp[i][0]) % MOD
    
    # The answer is the number of valid sequences minus the number of invalid ones
    result = (total_ways - invalid_ways + MOD) % MOD
    return result

def is_valid_subsequence(s, start, n):
    balance = 0
    for i in range(len(s)):
        if s[i] == '(':
            balance += 1
        else:
            balance -= 1
        if balance < 0 or balance > n:
            return False
    return balance == 0

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
s = data[1]

# Output the result
print(count_regular_bracket_sequences(n, s))