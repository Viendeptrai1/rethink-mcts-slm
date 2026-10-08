import sys

def max_monsters_defeated(N, A, B):
    # Initialize the DP array where dp[i] represents the maximum monsters defeated up to the i-th town
    dp = [0] * (N + 2)
    
    # Iterate over each hero
    for i in range(1, N + 1):
        # Calculate the maximum monsters the i-th hero can defeat
        # This is the minimum of B[i-1] and the sum of monsters in the i-th and (i+1)-th towns
        max_defeat = min(B[i-1], A[i-1] + A[i])
        
        # Update the DP array
        # The maximum monsters defeated up to the (i+1)-th town is either:
        # 1. The maximum monsters defeated up to the i-th town plus the monsters defeated by the i-th hero
        # 2. The maximum monsters defeated up to the (i+1)-th town without the i-th hero
        dp[i+1] = max(dp[i] + max_defeat, dp[i+1])
    
    # The answer is the maximum monsters defeated up to the (N+1)-th town
    return dp[N+1]

# Read input
input = sys.stdin.read
data = input().split()

N = int(data[0])
A = list(map(int, data[1:N+2]))
B = list(map(int, data[N+2:]))

# Print the result
print(max_monsters_defeated(N, A, B))