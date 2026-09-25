import sys

def max_profit_distribution(n, k, difficulties):
    # Initialize the dp array where dp[i][j] represents the maximum profit
    # achievable with the first i problems distributed over j days.
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Initialize the parent array to reconstruct the solution.
    parent = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Fill the dp table.
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            current_max = 0
            for l in range(i, 0, -1):
                current_max = max(current_max, difficulties[l - 1])
                if dp[l - 1][j - 1] + current_max > dp[i][j]:
                    dp[i][j] = dp[l - 1][j - 1] + current_max
                    parent[i][j] = l
    
    # Reconstruct the solution.
    result = []
    current = n
    for d in range(k, 0, -1):
        previous = parent[current][d]
        result.append(current - previous)
        current = previous
    
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