from itertools import combinations

def calculate_piano_sum(N, K, a):
    MOD = 1000000007
    total_sum = 0
    
    # Generate all combinations of K keys
    for combo in combinations(a, K):
        # Find the maximum value in the current combination
        max_value = max(combo)
        # Add the maximum value to the total sum
        total_sum += max_value
    
    # Return the result modulo 1000000007
    return total_sum % MOD

# Read input
N, K = map(int, input().split())
a = list(map(int, input().split()))

# Calculate and print the result
print(calculate_piano_sum(N, K, a))