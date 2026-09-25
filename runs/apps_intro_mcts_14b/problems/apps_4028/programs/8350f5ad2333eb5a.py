import sys
from collections import defaultdict

MOD = 10**9 + 7

def count_valid_sequences(n, s):
    # Calculate the number of ways to balance the prefix and suffix
    def count_balanced_ways(prefix, suffix):
        dp = defaultdict(int)
        dp[0] = 1
        for char in prefix:
            if char == '(':
                for k in list(dp.keys()):
                    dp[k + 1] += dp[k]
                    dp[k + 1] %= MOD
            else:
                for k in sorted(dp.keys(), reverse=True):
                    if k > 0:
                        dp[k - 1] += dp[k]
                        dp[k - 1] %= MOD
                        del dp[k]
        
        result = 0
        for char in suffix:
            if char == '(':
                for k in list(dp.keys()):
                    dp[k + 1] += dp[k]
                    dp[k + 1] %= MOD
            else:
                for k in sorted(dp.keys(), reverse=True):
                    if k > 0:
                        dp[k - 1] += dp[k]
                        dp[k - 1] %= MOD
                        del dp[k]
        
        return dp[0]
    
    # Find all positions where s can be placed
    def find_positions(s, n):
        positions = []
        for i in range(n - len(s) + 1):
            positions.append(i)
        return positions
    
    # Calculate the total number of valid sequences
    total_sequences = 0
    positions = find_positions(s, n)
    for start in positions:
        prefix = '(' * start + s
        suffix = ')' * (n - start - len(s))
        total_sequences += count_balanced_ways(prefix, suffix)
        total_sequences %= MOD
    
    return total_sequences

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