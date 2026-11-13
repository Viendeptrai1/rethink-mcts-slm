MOD = 998244353

def solve():
    N = int(input())
    robots = []
    for _ in range(N):
        x, d = map(int, input().split())
        robots.append((x, d))
    
    robots.sort()
    dp = [0] * (N + 1)
    dp[N] = 1
    
    for i in range(N - 1, -1, -1):
        x, d = robots[i]
        j = binary_search(robots, x + d)
        dp[i] = (dp[i + 1] + dp[j]) % MOD
    
    return dp[0]

def binary_search(robots, target):
    left, right = 0, len(robots)
    while left < right:
        mid = (left + right) // 2
        if robots[mid][0] < target:
            left = mid + 1
        else:
            right = mid
    return left

if __name__ == "__main__":
    print(solve())