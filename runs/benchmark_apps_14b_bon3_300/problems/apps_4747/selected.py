import sys

def expected_score(n, k):
    # Create a table to store the expected scores
    dp = [[0.0] * (k + 1) for _ in range(n + 1)]
    
    # Base case: if there's only one roll, the expected score is the average of all sides
    for i in range(1, n + 1):
        dp[i][1] = (i + 1) / 2
    
    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(2, k + 1):
            dp[i][j] = sum(dp[x][j - 1] for x in range(1, i + 1)) / i
    
    return dp[n][k]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    k = int(data[1])
    result = expected_score(n, k)
    print(f"{result:.7f}")

if __name__ == "__main__":
    main()