def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    a = list(map(int, data[1:N+1]))
    
    # dp[i][j] will store the maximum score difference the current player can achieve
    # from the subarray a[i:j+1]
    dp = [[0] * N for _ in range(N)]
    
    # Base case: when there's only one card, the current player takes it
    for i in range(N):
        dp[i][i] = a[i]
    
    # Fill the dp table
    for length in range(2, N + 1):  # length of the subarray
        for i in range(N - length + 1):
            j = i + length - 1
            # The current player can choose either the i-th or the j-th card
            dp[i][j] = max(a[i] - dp[i + 1][j], a[j] - dp[i][j - 1])
    
    # The result is the maximum score difference starting from the full array
    result = dp[0][N - 1]
    print(result)

if __name__ == "__main__":
    main()