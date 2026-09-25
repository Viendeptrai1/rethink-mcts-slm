import sys
from collections import defaultdict

MOD = 10**9 + 7

def catalan(n):
    if n == 0 or n == 1:
        return 1
    catalan_numbers = [0] * (n + 1)
    catalan_numbers[0] = 1
    catalan_numbers[1] = 1
    for i in range(2, n + 1):
        for j in range(i):
            catalan_numbers[i] = (catalan_numbers[i] + catalan_numbers[j] * catalan_numbers[i - j - 1]) % MOD
    return catalan_numbers[n]

def count_sequences(n, s):
    def count_ways(left, right, balance):
        if left > right:
            return 0
        if balance < 0 or balance > right - left + 1:
            return 0
        if left == right:
            return 1 if balance == 0 else 0
        if (left, right, balance) in memo:
            return memo[(left, right, balance)]
        result = (count_ways(left + 1, right, balance + 1) + count_ways(left + 1, right, balance - 1)) % MOD
        memo[(left, right, balance)] = result
        return result

    memo = {}
    total_ways = 0
    for i in range(len(s), 2 * n - len(s) + 1):
        left_ways = catalan(i // 2)
        right_ways = catalan((2 * n - len(s) - i) // 2)
        middle_ways = count_ways(0, len(s) - 1, 0)
        total_ways = (total_ways + left_ways * middle_ways * right_ways) % MOD
    return total_ways

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