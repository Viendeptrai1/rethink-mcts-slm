def max_profit(n, k, a):
    # Initialize variables
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    last_max = [-1] * (n + 1)
    
    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            dp[i][j] = max(dp[i - 1][j], dp[last_max[i - 1]][j - 1] + a[i - 1])
            if dp[i][j] > dp[i - 1][j]:
                last_max[i] = last_max[i - 1]
            else:
                last_max[i] = i - 1
    
    # Reconstruct the solution
    result = []
    current_day_problems = 0
    current_day_max = 0
    i = n
    while i > 0:
        if last_max[i] == i - 1:
            result.append(current_day_problems + 1)
            current_day_problems = 1
            current_day_max = a[i - 1]
            i -= 1
        else:
            current_day_problems += 1
            current_day_max = max(current_day_max, a[i - 1])
            i = last_max[i]
    
    # Output the results
    print(dp[n][k])
    print(' '.join(map(str, reversed(result))))

# Example usage
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:]))

max_profit(n, k, a)