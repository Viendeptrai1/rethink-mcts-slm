MOD = 10**9 + 7

def count_ways(n):
    # Calculate the total number of ways to distribute coins without any restrictions
    total_ways = pow(3, 3 * n, MOD)
    
    # Calculate the number of ways where Tanya is not satisfied
    # This happens when for all i, a[i] + a[i+n] + a[i+2n] == 6
    # We need to count the number of valid distributions for each i
    
    # There are 3 possible values for each gnome: 1, 2, or 3 coins
    # We need to find combinations where the sum is 6
    valid_combinations = 0
    for a in range(1, 4):
        for b in range(1, 4):
            for c in range(1, 4):
                if a + b + c == 6:
                    valid_combinations += 1
    
    # The number of ways where Tanya is not satisfied is valid_combinations^n
    not_satisfied_ways = pow(valid_combinations, n, MOD)
    
    # The number of ways where Tanya is satisfied is the total ways minus the not satisfied ways
    satisfied_ways = (total_ways - not_satisfied_ways) % MOD
    
    return satisfied_ways

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])

# Print the result
print(count_ways(n))