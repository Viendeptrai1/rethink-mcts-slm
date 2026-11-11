import sys

def max_monsters_defeated(N, A, B):
    # Initialize the DP array where dp[i] represents the maximum monsters defeated up to the i-th town
    dp = [0] * (N + 2)
    
    # Iterate over each hero
    for i in range(1, N + 1):
        # Calculate the maximum monsters that can be defeated if the i-th hero helps the (i-1)-th town
        dp[i] = max(dp[i], dp[i - 1])
        # Calculate the maximum monsters that can be defeated if the i-th hero helps the i-th town
        dp[i + 1] = max(dp[i + 1], dp[i - 1] + min(B[i - 1], A[i - 1] + A[i]))
    
    # The answer is the maximum value in the dp array up to the (N+1)-th town
    return dp[N + 1]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    A = list(map(int, data[1:N + 2]))
    B = list(map(int, data[N + 2:2 * N + 2]))
    
    result = max_monsters_defeated(N, A, B)
    print(result)

if __name__ == "__main__":
    main()