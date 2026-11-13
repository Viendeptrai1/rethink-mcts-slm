def max_elements(p):
    n = len(p)
    dp = [0] * (n + 1)
    
    for i in range(n - 1, -1, -1):
        dp[i] = 1
        for j in range(i + 1, n):
            if p[i:j+1].startswith(str(int(p[j]))):
                dp[i] = max(dp[i], dp[j] + 1)
                
    return dp[0]

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    p = data[0]
    print(max_elements(p))