MOD = 10**9 + 7

def catalan(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result = result * i // (i - n)
    return result % MOD

def count_sequences(n, s):
    def count_ways_to_balance(prefix, balance):
        if balance < 0 or balance > len(prefix):
            return 0
        if len(prefix) == 0:
            return 1 if balance == 0 else 0
        if (prefix, balance) in memo:
            return memo[(prefix, balance)]
        
        ways = 0
        if prefix[0] == '(':
            ways += count_ways_to_balance(prefix[1:], balance + 1)
        elif prefix[0] == ')':
            ways += count_ways_to_balance(prefix[1:], balance - 1)
        
        memo[(prefix, balance)] = ways % MOD
        return ways
    
    total_ways = 0
    for i in range(len(s), 2 * n - len(s) + 1):
        left_length = i
        right_length = 2 * n - len(s) - i
        
        left_ways = catalan(left_length // 2)
        right_ways = catalan(right_length // 2)
        
        memo = {}
        middle_ways = count_ways_to_balance(s, 0)
        
        total_ways += (left_ways * middle_ways * right_ways) % MOD
    
    return total_ways % MOD

import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
s = data[1]
print(count_sequences(n, s))