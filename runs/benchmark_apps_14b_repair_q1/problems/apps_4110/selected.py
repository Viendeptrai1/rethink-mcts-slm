def min_problems_to_solve(D, G, problems):
    # Initialize the dp array where dp[i] represents the minimum number of problems needed to achieve at least i points
    dp = [float('inf')] * (G + 1)
    dp[0] = 0
    
    # Iterate over each difficulty level
    for i in range(1, D + 1):
        pi, ci = problems[i-1]
        # Iterate over the possible scores we can achieve with the current difficulty level
        for j in range(G, -1, -1):
            # If we solve all problems of this difficulty level
            if j >= 100 * i * pi:
                dp[j] = min(dp[j], dp[j - 100 * i * pi] + pi)
            else:
                # Calculate the maximum score we can get without solving all problems of this difficulty level
                max_score_without_all = (j // (100 * i)) * 100 * i
                dp[j] = min(dp[j], dp[max_score_without_all] + (j // (100 * i)))
    
    # Find the minimum number of problems needed to achieve at least G points
    for i in range(G, -1, -1):
        if dp[i] != float('inf'):
            return dp[i]

# Read input
import sys
input = sys.stdin.read
data = input().split()

D = int(data[0])
G = int(data[1])
problems = []

index = 2
for _ in range(D):
    pi = int(data[index])
    ci = int(data[index + 1])
    problems.append((pi, ci))
    index += 2

# Solve the problem
result = min_problems_to_solve(D, G, problems)

# Print the result
print(result)