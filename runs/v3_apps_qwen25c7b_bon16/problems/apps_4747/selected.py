import sys

def expected_score(n, k):
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        dp[i][1] = i
    
    for rolls in range(2, k + 1):
        for faces in range(1, n + 1):
            dp[faces][rolls] = sum(dp[dice][rolls - 1] for dice in range(faces)) / faces
    
    return dp[n][k]

input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])

print(expected_score(n, k))