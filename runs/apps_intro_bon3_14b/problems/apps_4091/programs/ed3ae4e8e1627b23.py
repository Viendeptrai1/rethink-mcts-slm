import sys

def max_profit_distribution(n, k, difficulties):
    # Initialize the DP table
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    # Initialize the path table to reconstruct the solution
    path = [[0] * (k + 1) for _ in range(n + 1)]

    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            if j == 1:
                dp[i][j] = max(difficulties[:i])
                path[i][j] = i
            else:
                max_diff = 0
                best_split = 0
                for split in range(j - 1, i):
                    current_max = max(difficulties[split:i])
                    if dp[split][j - 1] + current_max > dp[i][j]:
                        dp[i][j] = dp[split][j - 1] + current_max
                        best_split = split
                path[i][j] = best_split

    # Reconstruct the solution
    result = []
    current = n
    for day in range(k, 0, -1):
        result.append(current - path[current][day])
        current = path[current][day]

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