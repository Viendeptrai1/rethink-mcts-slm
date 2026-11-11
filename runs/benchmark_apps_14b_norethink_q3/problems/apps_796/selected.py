MOD = 10**9 + 7

def count_ways(n, k):
    if n > k:
        return 0
    
    # Calculate (k - n + 1) ^ n % MOD
    result = pow(k - n + 1, n, MOD)
    
    # Calculate n! % MOD
    factorial = 1
    for i in range(2, n + 1):
        factorial = (factorial * i) % MOD
    
    # Calculate the modular inverse of n! % MOD
    inv_factorial = pow(factorial, MOD - 2, MOD)
    
    # Final result is (result * inv_factorial) % MOD
    return (result * inv_factorial) % MOD

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])

# Print the result
print(count_ways(n, k))