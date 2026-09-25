import sys

def max_profit_distribution(n, k, difficulties):
    # Initialize the dp array where dp[i][j] represents the maximum profit
    # achievable with the first i problems distributed over j days.
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Initialize the last_problem array to keep track of the last problem
    # included in the optimal solution for each dp[i][j].
    last_problem = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Fill the dp table
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            # Option 1: Start a new day with the i-th problem
            option1 = difficulties[i - 1]
            if j > 1:
                option1 += dp[i - 1][j - 1]
            
            # Option 2: Continue the previous day with the i-th problem
            option2 = dp[i - 1][j]
            if j > 1:
                option2 = max(option2, dp[i - 1][j - 1])
            
            # Choose the better option
            if option1 > option2:
                dp[i][j] = option1
                last_problem[i][j] = i
            else:
                dp[i][j] = option2
                last_problem[i][j] = last_problem[i - 1][j]
    
    # Reconstruct the solution
    result = []
    current = n
    for day in range(k, 0, -1):
        result.append(current - last_problem[current][day] + 1)
        current = last_problem[current][day] - 1
    
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