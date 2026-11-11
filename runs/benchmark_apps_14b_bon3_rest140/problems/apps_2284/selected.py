import sys
from typing import List

def min_cost(n: int, k: int, a: List[int], b: List[int]) -> int:
    # Initialize the DP table
    dp = [[float('inf')] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    
    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(k + 1):
            if j > 0:
                dp[i][j] = min(dp[i][j], dp[i - 1][j])
                dp[i][j] = min(dp[i][j], dp[i - 1][j - 1] + a[i - 1] + b[i - 1])
                if i > 1:
                    dp[i][j] = min(dp[i][j], dp[i - 2][j - 1] + a[i - 2] + b[i - 1])
    
    return dp[n][k]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:n+2]))
    b = list(map(int, data[n+2:2*n+2]))
    
    result = min_cost(n, k, a, b)
    print(result)

if __name__ == "__main__":
    main()