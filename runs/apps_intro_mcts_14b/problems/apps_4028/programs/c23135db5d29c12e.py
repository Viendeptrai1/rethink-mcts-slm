import sys
from collections import defaultdict

MOD = 10**9 + 7

def count_valid_sequences(n, s):
    def catalan_number(n):
        if n <= 1:
            return 1
        res_num = 1
        res_den = 1
        for i in range(2, n + 1):
            res_num *= (n + i)
            res_den *= i
        return res_num // res_den % MOD

    def count_ways_to_embed(s):
        n = len(s)
        dp = [[0] * (n + 1) for _ in range(n + 1)]
        dp[0][0] = 1

        for i in range(n):
            for j in range(i + 1):
                if s[i] == '(':
                    dp[i + 1][j] += dp[i][j]
                    dp[i + 1][j + 1] += dp[i][j]
                else:
                    if j > 0:
                        dp[i + 1][j - 1] += dp[i][j]
                dp[i + 1][j] %= MOD
                dp[i + 1][j + 1] %= MOD

        return dp[n][0]

    total_length = 2 * n
    s_length = len(s)

    if s_length > total_length:
        return 0

    # Calculate the number of ways to embed s in a sequence of length total_length
    ways_to_embed_s = count_ways_to_embed(s)

    # Calculate the number of valid sequences of length total_length - s_length
    remaining_length = total_length - s_length
    valid_sequences_count = catalan_number(remaining_length // 2)

    # The result is the product of the two counts
    result = (ways_to_embed_s * valid_sequences_count) % MOD

    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    s = data[1]
    result = count_valid_sequences(n, s)
    print(result)

if __name__ == "__main__":
    main()