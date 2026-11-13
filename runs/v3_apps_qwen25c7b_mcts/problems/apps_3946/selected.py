MOD = 998244353

def mod_inv(a):
    return pow(a, MOD - 2, MOD)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    a = list(map(int, data[2:n+2]))
    w = list(map(int, data[n+2:2*n+2]))
    
    total_weight = sum(w)
    dp = [total_weight] * (n + 1)
    
    for _ in range(m):
        new_dp = [0] * (n + 1)
        for i in range(n):
            if a[i] == 1:
                new_dp[i + 1] += w[i]
            else:
                new_dp[i] -= w[i]
        dp = [new_dp[j] + dp[j] for j in range(n + 1)]
    
    result = []
    for i in range(n):
        numerator = dp[i + 1] * mod_inv(total_weight)
        result.append(numerator % MOD)
    
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()