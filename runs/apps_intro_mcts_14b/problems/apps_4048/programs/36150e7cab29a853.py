import sys
import math

def min_moves_to_reach_N(N):
    # Function to count the number of divisors of N
    def count_divisors(n):
        count = 0
        for i in range(1, int(math.sqrt(n)) + 1):
            if n % i == 0:
                if i * i == n:
                    count += 1
                else:
                    count += 2
        return count
    
    # Find the smallest divisor greater than 1
    for i in range(2, N + 1):
        if N % i == 0:
            return i + (N // i) - 2

# Read input from standard input
N = int(sys.stdin.read().strip())

# Calculate and print the result
print(min_moves_to_reach_N(N))