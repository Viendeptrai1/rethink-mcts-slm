import sys
from collections import defaultdict

MOD = 10**9 + 7

def count_sequences(n, s):
    def catalan(n):
        if n <= 1:
            return 1
        res_num = 1
        res_den = 1
        for i in range(2, n + 1):
            res_num *= (n + i)
            res_den *= i
        return res_num // res_den % MOD

    def dp_with_substring(n, s):
        m = len(s)
        dp = defaultdict(int)
        dp[(0, 0)] = 1

        for i in range(1, 2 * n + 1):
            for j in range(-i, i + 1, 2):
                if j - 1 >= 0:
                    dp[(i, j)] += dp[(i - 1, j - 1)]
                    dp[(i, j)] %= MOD
                if j + 1 <= 0:
                    dp[(i, j)] += dp[(i - 1, j + 1)]
                    dp[(i, j)] %= MOD

        count = 0
        for i in range(m, 2 * n + 1):
            for j in range(-i, i + 1, 2):
                if dp[(i, j)] > 0 and j == m - 2 * s.count(')') + 2 * s.count('('):
                    count += dp[(i, j)]
                    count %= MOD

        return count

    return dp_with_substring(n, s)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    s = data[1]
    result = count_sequences(n, s)
    print(result)

if __name__ == "__main__":
    main()