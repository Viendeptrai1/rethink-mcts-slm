import sys
from typing import List

def max_profit_distribution(n: int, k: int, difficulties: List[int]) -> None:
    # Initialize the DP table
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    # Initialize the path table to reconstruct the solution
    path = [[0] * (k + 1) for _ in range(n + 1)]

    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            max_difficulty = 0
            for l in range(j, i + 1):
                max_difficulty = max(max_difficulty, difficulties[l - 1])
                if dp[i - l][j - 1] + max_difficulty > dp[i][j]:
                    dp[i][j] = dp[i - l][j - 1] + max_difficulty
                    path[i][j] = l

    # Reconstruct the solution
    result = []
    current = n
    days = k
    while current > 0:
        result.append(path[current][days])
        current -= path[current][days]
        days -= 1

    # Print the maximum profit
    print(dp[n][k])
    # Print the distribution of problems
    print(" ".join(map(str, result[::-1])))

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    difficulties = list(map(int, data[2:]))
    
    max_profit_distribution(n, k, difficulties)