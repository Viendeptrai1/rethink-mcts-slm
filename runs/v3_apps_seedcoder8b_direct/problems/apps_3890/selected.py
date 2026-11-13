def count_valid_plaques(n, k):
    MOD = 1000000007

    # Function to calculate the number of valid sequences for a given starting house
    def count_sequences(start):
        sequence = []
        current = start
        while current not in sequence:
            sequence.append(current)
            current = plaques[current - 1]
        cycle_start = sequence.index(current)
        cycle_length = len(sequence) - cycle_start
        return cycle_length

    # Initialize the DP table
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    dp[1][1] = 1

    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if dp[i][j] > 0:
                next_house = plaques[j - 1]
                dp[i + 1][next_house] = (dp[i + 1][next_house] + dp[i][j]) % MOD

    # Calculate the result
    result = 0
    for i in range(1, k + 1):
        result = (result + dp[n][i]) % MOD

    return result

# Read input
n, k = map(int, input().split())

# Initialize the plaques array
plaques = [0] * n

# Generate all valid plaque configurations
def generate_plaques(index):
    if index == n:
        return count_valid_plaques(n, k)
    
    total = 0
    for i in range(1, n + 1):
        plaques[index] = i
        total = (total + generate_plaques(index + 1)) % MOD
    
    return total

# Calculate and print the result
print(generate_plaques(0))