import sys
from typing import List

def max_profit_distribution(n: int, k: int, difficulties: List[int]) -> None:
    # Initialize the dp table
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    # Initialize the parent table to reconstruct the solution
    parent = [[0] * (k + 1) for _ in range(n + 1)]

    # Fill the dp table
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            max_difficulty = 0
            for l in range(i, 0, -1):
                max_difficulty = max(max_difficulty, difficulties[l - 1])
                if dp[l - 1][j - 1] + max_difficulty > dp[i][j]:
                    dp[i][j] = dp[l - 1][j - 1] + max_difficulty
                    parent[i][j] = l

    # Reconstruct the solution
    result = []
    current = n
    for d in range(k, 0, -1):
        previous = parent[current][d]
        result.append(current - previous + 1)
        current = previous - 1

    # Print the maximum profit
    print(dp[n][k])
    # Print the distribution of problems
    print(' '.join(map(str, result[::-1])))

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    difficulties = list(map(int, data[2:]))
    
    max_profit_distribution(n, k, difficulties)