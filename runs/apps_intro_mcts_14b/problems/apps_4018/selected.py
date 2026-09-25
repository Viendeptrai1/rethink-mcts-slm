import sys

def main():
    import sys
    import math
    
    def count_distinct_subsequences(s):
        n = len(s)
        mod = 10**9 + 7
        dp = [0] * (n + 1)
        dp[0] = 1
        last = {}
        
        for i in range(1, n + 1):
            dp[i] = (2 * dp[i - 1]) % mod
            if s[i - 1] in last:
                dp[i] = (dp[i] - dp[last[s[i - 1]] - 1] + mod) % mod
            last[s[i - 1]] = i
    
        return dp[n]
    
    def min_cost(n, k, s):
        distinct_count = count_distinct_subsequences(s)
        if k > distinct_count:
            return -1
        
        total_cost = 0
        current_size = 0
        
        while current_size < k:
            if current_size == 0:
                total_cost += 0
            else:
                total_cost += n - current_size
            current_size += 1
        
        return total_cost
    
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    s = data[2]
    
    result = min_cost(n, k, s)
    print(result)

if __name__ == "__main__":
    main()