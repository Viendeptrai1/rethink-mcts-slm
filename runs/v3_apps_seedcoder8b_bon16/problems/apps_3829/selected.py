import sys

def expected_maximum(m, n):
    if n == 1:
        return (m + 1) / 2
    
    dp = [0] * (m + 1)
    for i in range(1, m + 1):
        dp[i] = i
    
    for _ in range(2, n + 1):
        new_dp = [0] * (m + 1)
        for i in range(1, m + 1):
            new_dp[i] = i + (m - i + 1) / m * dp[i - 1]
        dp = new_dp
    
    return sum(dp) / m

def main():
    m, n = map(int, sys.stdin.readline().split())
    result = expected_maximum(m, n)
    print(f"{result:.12f}")

if __name__ == "__main__":
    main()