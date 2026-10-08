import sys

def count_good_plans(n, m, b, mod, a):
    dp = [[0] * (b + 1) for _ in range(m + 1)]
    dp[0][0] = 1
    
    for i in range(1, n + 1):
        new_dp = [[0] * (b + 1) for _ in range(m + 1)]
        for j in range(m + 1):
            for k in range(b + 1):
                for v in range(j + 1):
                    if k - v * a[i - 1] >= 0:
                        new_dp[j][k] = (new_dp[j][k] + dp[j - v][k - v * a[i - 1]]) % mod
        dp = new_dp
    
    return sum(dp[m]) % mod

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    b = int(data[2])
    mod = int(data[3])
    a = list(map(int, data[4:]))
    
    result = count_good_plans(n, m, b, mod, a)
    print(result)

if __name__ == "__main__":
    main()