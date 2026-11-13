def count_regular_bracket_sequences(n, s):
    MOD = 1000000007
    m = len(s)
    
    # dp[i][j] will store the number of ways to form a valid sequence of length i
    # with j more opening brackets than closing brackets
    dp = [[0] * (n + 1) for _ in range(2 * n + 1)]
    dp[0][0] = 1  # Base case: one way to form an empty sequence
    
    for i in range(1, 2 * n + 1):
        for j in range(n + 1):
            if j > 0:
                dp[i][j] = dp[i - 1][j - 1]  # Add an opening bracket
            if j < n:
                dp[i][j] = (dp[i][j] + dp[i - 1][j + 1]) % MOD  # Add a closing bracket
    
    # Now, we need to count the number of valid sequences that contain s as a substring
    count = 0
    for i in range(2 * n - m + 1):
        if dp[i][0] > 0:
            # Check if s can be placed at position i
            valid = True
            balance = 0
            for k in range(m):
                if s[k] == '(':
                    balance += 1
                else:
                    balance -= 1
                if balance < 0:
                    valid = False
                    break
            if valid and balance == 0:
                count = (count + dp[i][0]) % MOD
    
    return count

# Read input
n = int(input().strip())
s = input().strip()

# Calculate and print the result
result = count_regular_bracket_sequences(n, s)
print(result)