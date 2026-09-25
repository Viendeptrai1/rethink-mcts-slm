import sys
from collections import defaultdict

MOD = 10**9 + 7

def count_regular_sequences(n, s):
    # dp[i][j] will store the number of ways to form a regular bracket sequence of length i
    # with j unmatched opening brackets at the end
    dp = [[0] * (n + 1) for _ in range(2 * n + 1)]
    dp[0][0] = 1

    # Precompute the number of ways to close j unmatched opening brackets
    close_ways = [0] * (n + 1)
    close_ways[0] = 1
    for j in range(1, n + 1):
        close_ways[j] = (close_ways[j - 1] * (2 * j - 1)) % MOD

    # Iterate over all possible lengths of the sequence
    for i in range(1, 2 * n + 1):
        for j in range(n + 1):
            if j > 0:
                dp[i][j] = (dp[i][j] + dp[i - 1][j - 1]) % MOD
            if j < n:
                dp[i][j] = (dp[i][j] + dp[i - 1][j + 1]) % MOD

    # Find the positions where s can start in a sequence of length 2n
    count = 0
    for start in range(2 * n - len(s) + 1):
        valid = True
        balance = 0
        for k in range(len(s)):
            if s[k] == '(':
                balance += 1
            else:
                balance -= 1
            if balance < 0:
                valid = False
                break
        if valid:
            # Calculate the number of ways to form the sequence before and after s
            left_length = start
            right_length = 2 * n - start - len(s)
            left_balance = 0
            for k in range(start):
                if s[k] == '(':
                    left_balance += 1
                else:
                    left_balance -= 1
            right_balance = 0
            for k in range(start + len(s), 2 * n):
                if s[k] == '(':
                    right_balance += 1
                else:
                    right_balance -= 1
            if left_balance >= 0 and right_balance >= 0:
                count = (count + dp[left_length][left_balance] * dp[right_length][right_balance] * close_ways[left_balance] * close_ways[right_balance]) % MOD

    return count

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    s = data[1]
    result = count_regular_sequences(n, s)
    print(result)

if __name__ == "__main__":
    main()