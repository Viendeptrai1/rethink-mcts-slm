import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    M = int(data[1])
    
    broken = set()
    idx = 2
    for _ in range(M):
        broken.add(int(data[idx]))
        idx += 1
    
    MOD = 1_000_000_007
    
    dp = [0] * (N + 1)
    dp[0] = 1
    
    for i in range(1, N + 1):
        if i in broken:
            dp[i] = 0
            continue
        
        # From step i-1
        if i - 1 >= 0:
            dp[i] = (dp[i] + dp[i - 1]) % MOD
        
        # From step i-2
        if i - 2 >= 0:
            dp[i] = (dp[i] + dp[i - 2]) % MOD
    
    print(dp[N])

if __name__ == "__main__":
    solve()