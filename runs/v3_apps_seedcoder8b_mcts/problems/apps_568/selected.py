def count_ways(n):
    MOD = 10**9 + 7
    
    # Calculate the number of ways to distribute coins such that Tanya is satisfied
    # Total ways to distribute coins to 3n gnomes with 1 to 3 coins each
    total_ways = pow(3, 3 * n, MOD)
    
    # Calculate the number of invalid configurations
    # For each invalid configuration, we need to count the number of ways to form it
    invalid_ways = 0
    
    # Iterate over all possible starting points of the invalid triplet
    for i in range(3 * n):
        # Calculate the number of invalid triplets starting at i
        # The triplet consists of (i, i+1, i+2)
        # We need to ensure that a_i + a_{i+1} + a_{i+2} ≠ 6
        # This can happen in 3 cases:
        # 1. a_i + a_{i+1} + a_{i+2} = 0
        # 2. a_i + a_{i+1} + a_{i+2} = 1
        # 3. a_i + a_{i+1} + a_{i+2} = 2
        # For each case, we need to count the number of ways to form this triplet
        
        # Case 1: a_i + a_{i+1} + a_{i+2} = 0
        # This can happen in 1 way: (0, 0, 0)
        invalid_ways += 1
        
        # Case 2: a_i + a_{i+1} + a_{i+2} = 1
        # This can happen in 3 ways: (1, 0, 0), (0, 1, 0), (0, 0, 1)
        invalid_ways += 3
        
        # Case 3: a_i + a_{i+1} + a_{i+2} = 2
        # This can happen in 3 ways: (2, 0, 0), (0, 2, 0), (0, 0, 2)
        invalid_ways += 3
    
    # Since we counted each invalid triplet 3n times (once for each starting point),
    # we need to divide by 3n
    invalid_ways = (invalid_ways * pow(3 * n, MOD - 2, MOD)) % MOD
    
    # The number of valid configurations is the total number of configurations minus the number of invalid ones
    valid_ways = (total_ways - invalid_ways + MOD) % MOD
    
    return valid_ways

# Read input
n = int(input().strip())

# Calculate and print the result
print(count_ways(n))