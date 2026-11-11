MOD = 10**9 + 7

def catalan(n):
    if n <= 1:
        return 1
    res_num = 1
    res_den = 1
    for i in range(2, n + 1):
        res_num *= (n + i)
        res_den *= i
    return res_num // res_den % MOD

def count_sequences(n, s):
    def count_ways_to_balance(s):
        ways = [0] * (len(s) + 1)
        ways[0] = 1
        balance = 0
        for char in s:
            if char == '(':
                balance += 1
            else:
                balance -= 1
            if balance < 0:
                break
            ways[balance] += ways[balance - 1]
            ways[balance] %= MOD
        return ways[0]

    total_length = 2 * n
    s_length = len(s)
    if s_length > total_length:
        return 0

    left_length = (total_length - s_length) // 2
    right_length = total_length - s_length - left_length

    left_ways = catalan(left_length)
    right_ways = catalan(right_length)

    balanced_ways = count_ways_to_balance(s)

    result = (left_ways * right_ways * balanced_ways) % MOD
    return result

import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
s = data[1]
print(count_sequences(n, s))