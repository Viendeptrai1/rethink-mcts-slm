MOD = 10**9 + 7

def catalan(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    for i in range(2, n + 1):
        result //= i
    return result

def count_sequences(n, s):
    def count_ways_to_balance(s):
        open_count = 0
        close_count = 0
        ways = [0] * (len(s) + 1)
        ways[0] = 1
        for char in s:
            if char == '(':
                open_count += 1
            else:
                close_count += 1
            if open_count < close_count:
                break
            ways[open_count - close_count] += ways[open_count - close_count - 1]
            ways[open_count - close_count] %= MOD
        return ways[0]

    total_length = 2 * n
    s_length = len(s)
    if s_length > total_length:
        return 0

    # Calculate the number of ways to place s in a sequence of length 2n
    count = 0
    for start in range(total_length - s_length + 1):
        left_part = s[:start]
        right_part = s[start + s_length:]
        left_open = left_part.count('(')
        left_close = left_part.count(')')
        right_open = right_part.count('(')
        right_close = right_part.count(')')

        if left_open >= left_close and right_open >= right_close:
            left_balance = count_ways_to_balance(left_part)
            right_balance = count_ways_to_balance(right_part)
            count += (catalan(left_open - left_close) * catalan(right_open - right_close) * left_balance * right_balance) % MOD
            count %= MOD

    return count

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
s = data[1]

# Output the result
print(count_sequences(n, s))