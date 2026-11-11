MOD = 10**9 + 7

def count_ways(n):
    # Calculate the total number of ways to distribute coins without any restrictions
    total_ways = pow(3, 3 * n, MOD)
    
    # Calculate the number of ways where Tanya is not satisfied
    # This happens when for all i, a_i + a_(i+n) + a_(i+2n) == 6
    # We need to count the number of valid distributions for each i
    invalid_ways = 0
    
    # For each possible value of a_i, a_(i+n), a_(i+2n)
    for a in range(1, 4):
        for b in range(1, 4):
            for c in range(1, 4):
                if a + b + c == 6:
                    invalid_ways += 1
    
    # Since there are n such triplets, we need to raise the invalid_ways to the power of n
    invalid_ways = pow(invalid_ways, n, MOD)
    
    # The number of ways where Tanya is satisfied is the total ways minus the invalid ways
    valid_ways = (total_ways - invalid_ways) % MOD
    
    return valid_ways

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])

# Print the result
print(count_ways(n))