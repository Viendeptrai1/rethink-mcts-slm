import sys

def max_profit(n, k, difficulties):
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
                current_max = 0
                for l in range(j - 1, i):
                    current_max = max(current_max, difficulties[l])
                    if dp[l][j - 1] + current_max > dp[i][j]:
                        dp[i][j] = dp[l][j - 1] + current_max
                        path[i][j] = i - l

    # Reconstruct the solution
    result = []
    current = n
    for d in range(k, 0, -1):
        result.append(path[current][d])
        current -= path[current][d]

    return dp[n][k], result[::-1]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    difficulties = list(map(int, data[2:]))
    
    max_profit_value, distribution = max_profit(n, k, difficulties)
    
    print(max_profit_value)
    print(' '.join(map(str, distribution)))

if __name__ == "__main__":
    main()