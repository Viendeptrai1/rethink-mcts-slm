import sys

def max_profit_distribution(n, k, difficulties):
    # Initialize the DP table
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    prev = [[0] * (k + 1) for _ in range(n + 1)]

    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            max_difficulty = 0
            for l in range(i, 0, -1):
                max_difficulty = max(max_difficulty, difficulties[l - 1])
                if dp[l - 1][j - 1] + max_difficulty > dp[i][j]:
                    dp[i][j] = dp[l - 1][j - 1] + max_difficulty
                    prev[i][j] = l

    # Reconstruct the solution
    result = []
    current = n
    for day in range(k, 0, -1):
        result.append(current - prev[current][day] + 1)
        current = prev[current][day] - 1

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
    print(" ".join(map(str, distribution)))

if __name__ == "__main__":
    main()