import sys
from collections import defaultdict

MOD = 10**9 + 7

def count_regular_sequences(n, s):
    def catalan(n):
        if n == 0:
            return 1
        res_num = 1
        res_den = 1
        for i in range(2, n + 1):
            res_num *= (n + i)
            res_den *= i
        return res_num // res_den

    def count_ways_to_insert(s):
        n = len(s)
        dp = [[0] * (n + 1) for _ in range(n + 1)]
        dp[0][0] = 1

        for i in range(n):
            for j in range(i + 1):
                if s[i] == '(':
                    dp[i + 1][j + 1] += dp[i][j]
                    dp[i + 1][j + 1] %= MOD
                else:
                    if j > 0:
                        dp[i + 1][j - 1] += dp[i][j]
                        dp[i + 1][j - 1] %= MOD

        return dp[n][0]

    total_length = 2 * n
    s_length = len(s)
    remaining_length = total_length - s_length

    if remaining_length < 0:
        return 0

    ways_to_insert = count_ways_to_insert(s)
    catalan_number = catalan(remaining_length // 2)

    result = (ways_to_insert * catalan_number) % MOD
    return result

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