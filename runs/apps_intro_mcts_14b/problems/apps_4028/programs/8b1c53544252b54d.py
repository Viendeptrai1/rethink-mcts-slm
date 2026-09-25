import sys

MOD = 10**9 + 7

def count_ways(n, s):
    # Precompute binomial coefficients
    binom = [[0] * (2 * n + 1) for _ in range(2 * n + 1)]
    for i in range(2 * n + 1):
        binom[i][0] = binom[i][i] = 1
        for j in range(1, i):
            binom[i][j] = (binom[i - 1][j - 1] + binom[i - 1][j]) % MOD

    # Function to count valid sequences of length m with k open brackets
    def count_sequences(m, k):
        if m < 0 or k < 0 or k > m:
            return 0
        return binom[m][k]

    # Length of the substring s
    len_s = len(s)
    
    # Count the number of valid sequences
    total_ways = 0
    
    # Iterate over all possible positions where s can start
    for start in range(2 * n - len_s + 1):
        # Check if s is a valid substring in a regular bracket sequence
        valid = True
        balance = 0
        for i in range(start, start + len_s):
            if s[i - start] == '(':
                balance += 1
            else:
                balance -= 1
            if balance < 0:
                valid = False
                break
        
        if valid and balance == 0:
            # Calculate the number of ways to form the sequence before s
            left_open = start // 2
            left_close = start // 2 - balance
            left_ways = count_sequences(start, left_open)
            
            # Calculate the number of ways to form the sequence after s
            right_open = (2 * n - start - len_s) // 2
            right_close = (2 * n - start - len_s) // 2 - balance
            right_ways = count_sequences(2 * n - start - len_s, right_open)
            
            # Total ways for this position
            total_ways = (total_ways + (left_ways * right_ways) % MOD) % MOD
    
    return total_ways

# Read input
n = int(sys.stdin.readline())
s = sys.stdin.readline().strip()

# Output the result
print(count_ways(n, s))