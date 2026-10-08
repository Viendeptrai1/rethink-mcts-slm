MOD = 10**9 + 7

def catalan(n):
    if n == 0:
        return 1
    res_num = 1
    res_den = 1
    for i in range(2, n + 1):
        res_num *= (n + i)
        res_den *= i
    return res_num // res_den % MOD

def count_ways_to_place_s(s, n):
    ways = [0] * (n + 1)
    ways[0] = 1
    open_count = 0
    close_count = 0
    for char in s:
        if char == '(':
            open_count += 1
        else:
            close_count += 1
        if open_count < close_count:
            break
        ways[open_count - close_count] += 1
        ways[open_count - close_count] %= MOD
    return ways

def count_regular_sequences_with_substring(n, s):
    total_length = 2 * n
    s_length = len(s)
    if s_length > total_length:
        return 0
    
    # Calculate the number of ways to place s in a sequence of length total_length
    ways_to_place_s = count_ways_to_place_s(s, n)
    
    # Calculate the number of valid bracket sequences of length total_length - s_length
    remaining_length = total_length - s_length
    if remaining_length % 2 != 0:
        return 0
    half_remaining_length = remaining_length // 2
    valid_sequences_count = catalan(half_remaining_length)
    
    # Calculate the result
    result = 0
    for i in range(len(ways_to_place_s)):
        if i <= half_remaining_length:
            result += ways_to_place_s[i] * catalan(i) * catalan(half_remaining_length - i)
            result %= MOD
    
    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
s = data[1]

# Output the result
print(count_regular_sequences_with_substring(n, s))