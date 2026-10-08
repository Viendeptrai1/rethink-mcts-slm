MOD = 10**9 + 7

def count_ways(n):
    # Total number of ways to distribute coins without any restrictions
    total_ways = 3**(3*n)
    
    # Number of ways that do not satisfy Tanya's condition
    invalid_ways = 0
    
    # Iterate over all possible values of a_i, a_i+n, a_i+2n
    for a_i in range(1, 4):
        for a_i_n in range(1, 4):
            for a_i_2n in range(1, 4):
                if a_i + a_i_n + a_i_2n == 6:
                    invalid_ways += 1
    
    # Calculate the number of valid ways
    valid_ways = total_ways - invalid_ways
    
    # Return the result modulo 10^9 + 7
    return valid_ways % MOD

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])

# Print the result
print(count_ways(n))