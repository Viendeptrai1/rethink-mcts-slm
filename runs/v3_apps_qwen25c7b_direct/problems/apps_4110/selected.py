import sys
input = sys.stdin.read
data = input().split()

D = int(data[0])
G = int(data[1])

problems = []
for i in range(D):
    p = int(data[2 * i + 2])
    c = int(data[2 * i + 3])
    problems.append((p, c))

def min_problems_to_solve(problems, G):
    dp = [float('inf')] * (G + 1)
    dp[0] = 0
    
    for p, c in problems:
        for g in range(G, -1, -1):
            if g >= p:
                dp[g] = min(dp[g], dp[g - p] + 1)
    
    for g in range(G, -1, -1):
        if dp[g] != float('inf'):
            return dp[g]
    
    return -1

result = min_problems_to_solve(problems, G)
print(result)