import sys

def max_profit_distribution(n, k, difficulties):
    # Initialize the DP table
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    # Initialize the parent table to reconstruct the solution
    parent = [[0] * (k + 1) for _ in range(n + 1)]

    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            max_difficulty = 0
            for l in range(j, i + 1):
                max_difficulty = max(max_difficulty, difficulties[l - 1])
                if dp[i - l][j - 1] + max_difficulty > dp[i][j]:
                    dp[i][j] = dp[i - l][j - 1] + max_difficulty
                    parent[i][j] = l

    # Reconstruct the solution
    result = []
    current = n
    days = k
    while days > 0:
        result.append(parent[current][days])
        current -= parent[current][days]
        days -= 1

    return dp[n][k], result[::-1]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    difficulties = list(map(int, data[2:]))
    
    max_profit, distribution = max_profit_distribution(n, k, difficulties)
    
    print(max_profit)
    print(' '.join(map(str, distribution)))

if __name__ == "__main__":
    main()