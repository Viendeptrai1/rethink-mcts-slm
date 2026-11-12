import math
from sys import stdin, stdout

def find_sequence(n, k):
    if n < k or k == 1:
        return -1
    
    # Start with the smallest possible values for the sequence
    sequence = [i for i in range(1, k + 1)]
    
    # Calculate the current sum and GCD of the initial sequence
    current_sum = sum(sequence)
    gcd_value = math.gcd(*sequence)
    
    # Adjust the sequence to meet the target sum while maintaining the GCD
    remaining_sum = n - current_sum
    for i in range(k - 1, 0, -1):
        if remaining_sum >= sequence[i]:
            sequence[i] += remaining_sum
            break
        else:
            gcd_value //= math.gcd(gcd_value, sequence[i])
            remaining_sum -= sequence[i]
            sequence[i] = 1
    
    # Check if the final sequence meets the requirements
    if sum(sequence) != n or math.gcd(*sequence) != gcd_value:
        return -1
    
    return sequence

# Read input
n, k = map(int, stdin.readline().strip().split())

# Find and print the result
result = find_sequence(n, k)
if result == -1:
    stdout.write("-1\n")
else:
    stdout.write(" ".join(map(str, result)) + "\n")